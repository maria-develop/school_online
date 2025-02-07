from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ims.models import Course, Lesson, Subscription
from ims.paginations import CustomPageNumberPagination
from ims.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from ims.tasks import send_course_update_email
from users.permissions import IsModer, IsOwner


@method_decorator(
    name="list", decorator=swagger_auto_schema(operation_description="Список курсов")
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    @action(detail=True, methods=("post",))
    def update_course(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if course.update_course.filter(pk=request.user.pk).exists():
            course.update_course.remove(request.user)
        # else:
        #     course.update_course.add(request.user)
        #     send_course_update_email.delay(course.owner.email)
        else:
            course.update_course.add(request.user)
            """Отправляем уведомления, если обновления не было последние 4 часа:"""
            if not course.was_updated_recently():
                subscribers = course.subscriptions.all()
                emails = [sub.user.email for sub in subscribers]
                for email in emails:
                    send_course_update_email.delay(email)
        serializer = self.get_serializer(course)
        return Response(serializer.data)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer,)
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | ~IsModer,)


class SubscriptionAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = request.user
        course_id = request.query_params.get("id")
        if not course_id:
            return Response(
                {"error": "Не указан course_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, pk=course_id)
        is_subscribed = Subscription.objects.filter(user=user, course=course).exists()
        return Response({"is_subscribed": is_subscribed}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("id")
        new_name = request.data.get("name_subscription")

        if not course_id or not new_name:
            return Response(
                {"error": "Не указан course_id или name_subscription"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = get_object_or_404(Subscription, user=user, course_id=course_id)
        subscription.name_subscription = new_name
        subscription.save()

        return Response(
            {
                "message": "Подписка обновлена",
                "name_subscription": subscription.name_subscription,
            },
            status=status.HTTP_200_OK,
        )

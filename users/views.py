from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer

# class UserCreateAPIView(CreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#     def perform_create(self, serializer):
#         user = serializer.save(is_active=True)
#         user.set_password(user.password)
#         user.save()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AllowAny,)

    # def get_serializer_class(self):
    #     if (
    #             self.action == "retrieve"
    #             and self.request.user == User.objects.get(pk=self.kwargs.get("pk"))
    #             or self.request.user.is_superuser
    #     ):
    #         return UserDetailSerializer
    #     return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        #     elif self.action in ["update", "partial_update", "destroy"]:
        #         self.permission_classes = (IsAuthenticated, IsProfileOwner | IsAdminUser)
        #
        return super().get_permissions()


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ("payment_date",)
    ordering = ("-payment_date",)
    search_fields = ("amount",)

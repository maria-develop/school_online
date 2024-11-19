from rest_framework.viewsets import ModelViewSet

from ims.models import Course
from ims.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
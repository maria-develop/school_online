from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ims.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        # fields = ("id", "name_lesson", "description_lesson", "video_url")


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    lessons_count = SerializerMethodField()

    # def get_lessons(self, course):
    #     return [less.name_lesson for less in Lesson.objects.filter(lesson=course)]

    def get_lessons_count(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    # lessons = SerializerMethodField()
    # lessons_count = SerializerMethodField()
    #
    # def get_lessons(self, obj):
    #     """
    #     Возвращает только список названий уроков для курса.
    #     """
    #     return [lesson.name_lesson for lesson in Lesson.objects.filter(course=obj)]
    #
    # def get_lessons_count(self, obj):
    #     """
    #     Возвращает количество уроков, связанных с курсом.
    #     """
    #     return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_count", "lessons")

from rest_framework import serializers

from ims.models import Course, Lesson, Subscription
from ims.validators import YoutubeValidator, youtube_url_validator


class LessonSerializer(serializers.ModelSerializer):
    name_lesson = serializers.CharField(validators=[youtube_url_validator])

    class Meta:
        model = Lesson
        fields = "__all__"
        # fields = ("id", "name_lesson", "description_lesson", "video_url")


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lessons_count = serializers.SerializerMethodField()
    # name = serializers.CharField(validators=[YoutubeValidator])
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    # lessons = serializers.SerializerMethodField()
    # lessons_count = serializers.SerializerMethodField()
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
        validators = [YoutubeValidator(field='description')]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_count", "lessons")

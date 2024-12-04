from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ims.models import Course, Lesson, Subscription
from users.models import User


class LessonTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro", password="123we")
        self.course = Course.objects.create(name="Test Course", description='test')
        self.lesson = Lesson.objects.create(
            name_lesson="Test Lesson",
            course=self.course,
            owner=self.user,
            video_url="https://youtube.com/watch?v=test"
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('ims:lessons_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name_lesson'),
            self.lesson.name_lesson
        )

    def test_lesson_create(self):
        url = reverse('ims:lessons_create')
        data = {
            "name_lesson": "Курс тайского",
            "description_lesson": "Очень легкий",
            "video_url": "https://www.youtube.com/"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_update(self):
        url = reverse('ims:lessons_update', args=(self.lesson.pk,))
        data = {
            "name_lesson": "Курс тайского",
            "description_lesson": "Очень легкий",
            "video_url": "https://www.youtube.com/"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name_lesson'),
            "Курс тайского"
        )

    def test_lesson_delete(self):
        url = reverse('ims:lessons_delete', args=(self.lesson.pk,))

        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )

    def test_lesson_list(self):
        url = reverse('ims:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.lesson.pk,
                "video_url": self.lesson.video_url,
                "name_lesson": self.lesson.name_lesson,
                "preview_lesson": None,
                "description_lesson": None,
                "course": self.course.pk,
                "owner": self.user.pk
            }
        ]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )

    def test_invalid_url(self):
        url = reverse('ims:lessons_create')
        data = {
            "name_lesson": "Курс тайского",
            "description_lesson": "Очень легкий",
            "video_url": "https://invalid.com"
        }
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro", password="123we")
        self.course = Course.objects.create(name="Test Course", description='test')
        self.lesson = Lesson.objects.create(
            name_lesson="Test Lesson",
            course=self.course,
            owner=self.user,
            video_url="https://youtube.com/watch?v=test"
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_retrieve(self):
        url = reverse('ims:subscription') + f"?id={self.course.pk}"
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertIn("is_subscribed", data)
        self.assertFalse(data["is_subscribed"])  # Проверяем, что подписки ещё нет

        self.assertEqual(
            data.get('name'),
            None
        )

    def test_subscription_create(self):
        url = reverse('ims:subscription')
        data = {"id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.filter(user=self.user, course=self.course).count(),
            1
        )

    def test_subscription_update(self):
        # Создаем подписку
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            name_subscription="Старая подписка"
        )

        url = reverse('ims:subscription')
        data = {
            "id": self.course.pk,
            "name_subscription": "Курс тайского"
        }

        # Отправляем PATCH запрос
        response = self.client.patch(url, data)
        data_resp = response.json()

        # Проверяем статус ответа
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверяем данные в ответе
        self.assertEqual(
            data_resp.get('name_subscription'),
            "Курс тайского"
        )

        # Проверяем обновление в базе данных
        subscription.refresh_from_db()
        self.assertEqual(subscription.name_subscription, "Курс тайского")

    def test_subscription_delete(self):
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('ims:subscription')
        data = {"id": self.course.pk}
        response = self.client.post(url, data)  # Повторный POST должен удалить подписку

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.filter(user=self.user, course=self.course).count(),
            0  # Подписка удалена
        )

    def test_subscription_list(self):
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('ims:subscription') + f"?id={self.course.pk}"
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertTrue(data["is_subscribed"])  # Проверяем, что подписка существует

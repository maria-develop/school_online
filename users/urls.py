from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet)
router.register("users", UserViewSet)

urlpatterns = []
urlpatterns += router.urls

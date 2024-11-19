from rest_framework.routers import SimpleRouter

from ims.apps import ImsConfig
from ims.views import CourseViewSet

app_name = ImsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [

]
urlpatterns += router.urls
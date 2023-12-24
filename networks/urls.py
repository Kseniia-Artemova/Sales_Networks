from rest_framework.routers import DefaultRouter
from networks.views import TradeLinkViewSet

router = DefaultRouter()
router.register(r'networks', TradeLinkViewSet, basename='network')

urlpatterns = router.urls
from rest_framework import routers
from screenshots import viewsets

router = routers.DefaultRouter()


router.register(r'screenshot',
                viewsets.ScreenshotViewSet,
                base_name='screenshots-screenshot')

from rest_framework import routers
from screenshots import viewsets

router = routers.DefaultRouter()


router.register(r'screenshotsnapshot',
                viewsets.ScreenshotSnapshotViewSet,
                base_name='screenshots-screenshotsnapshot')

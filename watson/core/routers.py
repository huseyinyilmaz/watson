from rest_framework import routers
from core import viewsets

router = routers.DefaultRouter()

router.register(r'constants', viewsets.ConstantsViewSet,
                base_name='core-constants')

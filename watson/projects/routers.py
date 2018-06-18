from rest_framework import routers
from projects import viewsets

router = routers.DefaultRouter()

router.register(r'project', viewsets.ProjectViewSet, base_name='accounts-project')

from rest_framework import routers
from accounts import viewsets

router = routers.DefaultRouter()

router.register(r'users', viewsets.UserViewSet, base_name='accounts-users')
router.register(r'organizations', viewsets.OrganizationViewSet,
                base_name='accounts-organizations')
router.register(r'sessions', viewsets.SessionViewSet,
                base_name='accounts-sessions')

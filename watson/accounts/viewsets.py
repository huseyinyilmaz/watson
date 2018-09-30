from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# from accounts import models
from accounts import serializers
from core.permissions import CustomPermission

User = get_user_model()


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = ()

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        """If user is not admin user show only owned resources.

        Change this with isAdminOrSelf permission?
        """
        user = self.request.user
        queryset = User.objects.filter(pk=user.pk)
        return queryset


class OrganizationViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    permission_classes = (permissions.IsAuthenticated,
                          CustomPermission)
    serializer_class = serializers.OrganizationSerializer

    def has_object_permission(self, obj):
        return self.request.user.organizations.filter(id=obj.id).exists()

    def get_queryset(self):
        queryset = self.request.user.organizations.all()
        return queryset


class SessionViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    """
    Create and removes sessions.

    Based on this code
    https://github.com/JamesRitchie/django-rest-framework-sav/blob/a968129be88a1981d9904c3679e5fdd9490e890d/rest_framework_sav/views.py # noqa
    """

    lookup_field = 'key'
    permission_classes = ()
    serializer_class = serializers.SessionSerializer
    queryset = Token.objects.all()

    def get_response(self, request):
        """Return response for given view."""
        user = request.user
        logged_in = not user.is_anonymous
        response = {'logged_in': logged_in}
        if logged_in:
            userSerializer = serializers.UserSerializer(user)
            organizationSerializer = serializers.OrganizationSerializer(
                user.organizations.all(),
                many=True)

            response.update({
                'user': userSerializer.data,
                'organizations': organizationSerializer.data,
            })

        return response

    def retrieve(self, request, key=None):
        return Response({'key': key})

    def list(self, request):
        """List response."""
        return Response(self.get_response(request))

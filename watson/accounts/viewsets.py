from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# from accounts import models
from accounts import serializers

User = get_user_model()


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class SessionViewSet(mixins.CreateModelMixin,
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
            userSerializer = serializers.UserSerializer(
                user,
                context={'request': request})
            # profileSerializer = ProfileSerializer(
            #     user.profile,
            #     context={'request': request})
            response.update({
                'user': userSerializer.data,
                # 'profile': profileSerializer.data,
            })
        return response

    def list(self, request):
        """List response."""
        return Response(self.get_response(request))

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate

User = get_user_model()


class SessionSerializer(serializers.Serializer):

    """Session serializer that logs in user.

    based on rest_framework.authtoken.serializers.AuthTokenSerializer

    """

    # write_only_fields = ['email', 'password']
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """Create a token for user."""
        user = validated_data['user']
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return {'token': token.key}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from accounts.models import Organization
from accounts.models import Project
# from accounts.utils import generate_registration_code
from core.utils import get_slug


User = get_user_model()


class SessionSerializer(serializers.Serializer):

    """Session serializer that logs in user.

    based on rest_framework.authtoken.serializers.AuthTokenSerializer

    """

    # write_only_fields = ['email', 'password']
    email = serializers.EmailField(label=_("Email"), write_only=True)
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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        #  fields = ['email', 'password']
        fields = ['id', 'email', 'full_name',
                  'date_joined', 'email_verified',
                  'default_organization', 'password']
        extra_kwargs = {
            'default_organization': {'required': False},
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'email_verified': {'read_only': True},
        }


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'slug', 'name', 'company', 'location', 'email', 'url']


class ProjectSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        name = attrs.get('name')
        organization = attrs.get('organization')
        slug = get_slug(
            Project.objects.filter(organization=organization),
            name,
            )
        attrs['slug'] = slug
        return attrs

    class Meta:
        model = Project
        fields = ['id', 'slug', 'name', 'organization', 'default']
        extra_kwargs = {
            'slug': {'required': False, 'read_only': True},
        }


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(label=_("Full Name"))
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    organization_company = serializers.CharField(label=_("Company"),
                                                 required=False)
    organizatin_location = serializers.CharField(label=_("Location"),
                                                 required=False)
    organization_company_url = serializers.URLField(label=_("CompanyUrl"),
                                                    required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        name = attrs.get('email').split('@')[0]
        attrs['organization_name'] = name
        attrs['organization_slug'] = get_slug(Organization.objects.all(), name)
        return attrs

    def create(self, validated_data):
        organization_data = {
            'name': validated_data['organization_name'],
            'slug': validated_data['organization_slug'],
            'company': validated_data.get('organization_company', ''),
            'location': validated_data.get('organization_location', ''),
            'company_url': validated_data.get('organization_company_url', ''),
        }
        organization_serializer = OrganizationSerializer(
            data=organization_data)
        organization_serializer.is_valid(raise_exception=True)
        user_data = {
            'full_name': validated_data['name'],
            'email': validated_data['email'],
            'password': validated_data['password'],
            'organization': 1,
        }
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        # ================ Data is valid save objects ================
        organization = organization_serializer.save()
        user_data['default_organization'] = organization.pk
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.organizations.add(organization)
        return {
            'user': user_serializer,
            'organization': organization_serializer,
            'name': validated_data.get('name'),
            'email': validated_data.get('email'),
            'company': validated_data.get('company', ''),
            'location': validated_data.get('location', ''),
            'company_url': validated_data.get('company_url', ''),
        }

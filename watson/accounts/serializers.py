from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from accounts.models import Organization
from accounts.models import Project
# from accounts.utils import generate_registration_code
from core.utils import get_slug

import logging

logger = logging.getLogger(__name__)

User = get_user_model()


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

    def validate(self, attrs):
        user = self.context['request'].user
        name = attrs.get('name')
        slug = get_slug(
            user.organizations.all(),
            name,
        )
        attrs['slug'] = slug
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        user = self.context['request'].user
        user.organizations.add(instance)
        # User.objects.create_user(**validated_data)
        return instance

    class Meta:
        model = Organization
        fields = ['id', 'slug', 'name', 'company',
                  'location', 'email', 'url']
        extra_kwargs = {
            'slug': {'read_only': True},
            }


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


class SignupUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance

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


class SignupOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'slug', 'name', 'company', 'location', 'email', 'url']
        extra_kwargs = {
            'slug': {'required': False},
            'name': {'required': False},
        }


class SignupSerializer(serializers.Serializer):
    user = SignupUserSerializer()
    organization = SignupOrganizationSerializer()

    def validate(self, attrs):
        email = attrs['user'].get('email', '')
        attrs['organization']['name'] = email
        attrs['organization']['slug'] = get_slug(Organization.objects.all(),
                                                 email.split('@')[0])
        attrs['organization']['email'] = email
        return attrs

    def create(self, validated_data):
        logger.debug('SignupForm validated_data = %s', validated_data)
        organization_serializer = SignupOrganizationSerializer(
            data=validated_data['organization'])
        organization_serializer.is_valid(raise_exception=True)
        organization = organization_serializer.save()
        validated_data['user']['default_organization'] = organization.pk
        user_serializer = SignupUserSerializer(data=validated_data['user'])
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.organizations.add(organization)
        return {'user': user, 'organization': organization}


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

    key = serializers.CharField(label=_("token"), read_only=True)

    user = UserSerializer(read_only=True)
    organization = serializers.SerializerMethodField(read_only=True)
    project = serializers.SerializerMethodField(read_only=True)

    def get_organization_query(self, token):
        user = token.user
        organization_id = self.context['request'].GET.get('organization')
        query = user.organizations.all()
        if organization_id:
            query = query.filter(id=organization_id)
            if not query:
                msg = _('You do not have permission to get '
                        'data about this organization.')
                raise serializers.ValidationError(msg, code='invalid_data')
        return query

    def get_organization(self, token):
        user = token.user
        organization_id = self.context['request'].GET.get('organization')
        query = self.get_organization_query(token)
        if not organization_id:
            query = query.filter(id=user.default_organization.id)
        organization = query.first()
        if not organization:
            msg = _('You do not have permission to get '
                    'data about this organization.')
            raise serializers.ValidationError(msg, code='invalid_data')
        return OrganizationSerializer(instance=organization).data

    def get_project(self, token):
        organization_query = self.get_organization_query(token)
        project_id = self.context['request'].GET.get('project')
        if project_id:
            project = (Project.objects
                       .filter(id=project_id,
                               organization__in=organization_query)
                       .first())
            if not project:
                msg = _('You do not have permission to get '
                        'data about this project.')
                raise serializers.ValidationError(msg, code='invalid_data')
        else:
            project = Project.objects.filter(
                organization__in=organization_query,
                default=True).first()
            # organization_query.project.get(default=True)
        # user = token.user
        return ProjectSerializer(instance=project).data

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
        return token

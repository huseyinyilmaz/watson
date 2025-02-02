from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from accounts import models
from accounts import serializers
from rest_framework.serializers import ValidationError

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
                          mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.OrganizationSerializer

    # def has_object_permission(self, obj):
    #     return self.request.user.organizations.filter(id=obj.id).exists()

    def get_queryset(self):
        queryset = self.request.user.organizations.all()
        return queryset


class SignupViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    permission_classes = ()
    serializer_class = serializers.SignupSerializer


class SessionViewSet2(mixins.CreateModelMixin,
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
        project_id = request.GET.get('project')
        if project_id:
            project = (models.Project.objects
                       .filter(id=project_id)
                       .select_related('organization')
                       .first())
            if not project:
                raise Http404()
            organization = project.organization
        else:
            organization = user.default_organization
            project = organization.project_set.get(default=True)

        logged_in = not user.is_anonymous
        response = {'logged_in': logged_in}
        if logged_in:
            userSerializer = serializers.UserSerializer(user)
            organizationSerializer = serializers.OrganizationSerializer(
                organization,
                many=False)
            projectSerializer = serializers.ProjectSerializer(
                project,
                many=False)

            response.update({
                'user': userSerializer.data,
                'organization': organizationSerializer.data,
                'project': projectSerializer.data,
            })

        return response

    def retrieve(self, request, key=None):
        return Response({'key': key})

    def list(self, request):
        """List response."""
        return Response(self.get_response(request))


class SessionViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
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

    def get_queryset(self):
        user = self.request.user
        # import ipdb; ipdb.set_trace()
        if user.is_anonymous:
            return Token.objects.none()
        else:
            return Token.objects.filter(user=user)


class ProjectViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Creates new screenshot entry.

    A screenshot will probably take around 10 seconds to complete.
    After screenshot is ready, url will be added to image field on response.
    """
    serializer_class = serializers.ProjectSerializer

    def perform_destroy(self, instance):
        if instance.default:
            raise ValidationError({
                'detail': 'You cannot delete this project! '
                'Because it is default project '
                'for organization {}'.format(instance.organization.name)})
        else:
            super().perform_destroy(instance)

    def get_queryset(self):
        organization_id = self.request.query_params.get('organization')
        if organization_id:
            # make user has right to access organization.
            if (self.request.user.organizations
                    .filter(id=organization_id).exists()):
                projects = (models.Project.objects
                            .filter(organization=organization_id))
            else:
                # user does not belong to organization
                projects = models.Project.objects.none()
        else:
            organization_ids = self.request.user.organizations.values_list(
                'id', flat=True)
            # return screenshots that user can see.
            projects = (models.Project.objects
                        .filter(organization__in=organization_ids))

        return projects

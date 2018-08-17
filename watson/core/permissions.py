"""Permission implementations."""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    """Only allow owners of an object to edit it."""

    user_field = 'user'

    def has_object_permission(self, request, view, obj):
        """Allow update methods for owner.

        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        """
        return((request.method in permissions.SAFE_METHODS) or
               (getattr(obj, self.user_field) == request.user))


class CustomPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Allow methods for owner."""
        return view.has_object_permission(obj)

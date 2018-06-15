class OwnerFilterMixin(object):

    """Filters to own models."""

    user_field = 'user'

    def get_queryset(self):
        """If user is not admin user show only owned resources.

        Change this with isAdminOrSelf permission?
        """
        return super().get_queryset().filter(
            **{self.user_field: self.request.user})


class OwnerOrAdminFilterMixin(object):

    """Filters model to show only user's models."""

    user_field = 'user'

    def get_queryset(self):
        """If user is not admin user show only owned resources.

        Change this with isAdminOrSelf permission?
        """
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_staff or not user.is_superuser:
            queryset = queryset.filter(**{self.user_field: user})
        return queryset

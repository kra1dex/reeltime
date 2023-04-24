from rest_framework import permissions


class IsAdminOrPublished(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_superuser or not request.user.is_staff:
            queryset = view.get_queryset()
            queryset = queryset.filter(status='publish')
            view.queryset = queryset

        return True

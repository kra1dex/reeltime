from rest_framework import permissions


class IsAdminOrPublished(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        else:
            queryset = view.get_queryset()
            queryset = queryset.filter(status='publish')
            view.queryset = queryset
            return True

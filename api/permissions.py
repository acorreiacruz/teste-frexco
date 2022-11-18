from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "A User can only update and delete yourself"

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email
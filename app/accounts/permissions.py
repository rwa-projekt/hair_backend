from rest_framework import permissions

class AccountPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create': return True
        if request.user.is_authenticated:
            return True
        return False
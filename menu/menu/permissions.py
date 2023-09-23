from rest_framework import permissions

from menu.models import EmployeeProfile


class CanVotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return user.employee_profile is not None
        except EmployeeProfile.DoesNotExist:
            return False


class APIVersionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        version = request.META.get('HTTP_API_VERSION', 'latest')
        return version in ['latest']

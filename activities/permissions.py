from rest_framework.permissions import BasePermission


class FacilitatorInstructorPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser == True or request.user.is_staff == True


class StudentPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser == False and request.user.is_staff == False

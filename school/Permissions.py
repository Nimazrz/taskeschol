from rest_framework import permissions


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser and request.user.is_teacher


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser and not request.user.is_teacher
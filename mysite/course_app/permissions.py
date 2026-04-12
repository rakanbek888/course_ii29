from rest_framework.permissions import BasePermission

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'
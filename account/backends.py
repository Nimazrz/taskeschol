from account.models import Student
from django.contrib.auth.backends import BaseBackend


class StudentBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # First try to authenticate from the Student model
            user = Student.objects.get(username=username)
            if user.check_password(password):  # Check if password matches
                return user
        except Student.DoesNotExist:
            # If user not found in Student, return None
            return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None


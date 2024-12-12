from django.http import request
from django.utils import timezone
from rest_framework import serializers
from account.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from .models import *


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, max_length=50)
    first_name = serializers.CharField(write_only=True, max_length=50)
    last_name = serializers.CharField(write_only=True, max_length=50)
    meli_code = serializers.CharField(write_only=True, max_length=10, min_length=10)
    school = serializers.CharField(write_only=True, max_length=50, required=False)
    bio = serializers.CharField(write_only=True, max_length=500, required=False)
    is_teacher = serializers.BooleanField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        if Teacher.objects.filter(username=username).exists() or Student.objects.filter(username=username).exists():
            raise serializers.ValidationError("this username is taken")
        return attrs

    def create(self, validated_data):
        is_teacher = validated_data.pop('is_teacher')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        meli_code = validated_data.pop('meli_code')

        if not meli_code.isdigit():
            raise serializers.ValidationError({'meli_code': 'Meli code must be an integer.'})

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        validated_data['password'] = make_password(password)

        if is_teacher:
            user = Teacher.objects.create(meli_code=meli_code, **validated_data)
        else:
            user = Student.objects.create(meli_code=meli_code, **validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, max_length=50)
    password = serializers.CharField(write_only=True)

    def validate(self, request, *args, **kwargs):
        username = request.pop('username')
        password = request.pop('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        update_last_login(None, user)

        request['user'] = user
        return request


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'meli_code', 'school', 'bio', 'teacher']


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    meli_code = serializers.CharField(max_length=10, min_length=10)
    is_teacher = serializers.BooleanField(read_only=True)
    school = serializers.CharField(max_length=50, required=False)
    bio = serializers.CharField(max_length=500, required=False)
    students = StudentSerializer(many=True, read_only=True)

    students_to_add = serializers.ListField(
        child=serializers.CharField(max_length=10), required=False
    )
    students_to_remove = serializers.ListField(
        child=serializers.CharField(max_length=10), required=False
    )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.meli_code = validated_data.get('meli_code', instance.meli_code)
        instance.school = validated_data.get('school', instance.school)
        instance.bio = validated_data.get('bio', instance.bio)

        # Add students based on meli_code
        students_to_add = validated_data.get('students_to_add', [])
        for meli_code in students_to_add:
            try:
                student = Student.objects.get(meli_code=meli_code)
                instance.students.add(student)
            except Student.DoesNotExist:
                raise serializers.ValidationError(
                    {"students_to_add": f"Student with meli_code {meli_code} does not exist."}
                )

        # Remove students based on meli_code
        students_to_remove = validated_data.get('students_to_remove', [])
        for meli_code in students_to_remove:
            try:
                student = Student.objects.get(meli_code=meli_code)
                instance.students.remove(student)
            except Student.DoesNotExist:
                raise serializers.ValidationError(
                    {"students_to_remove": f"Student with meli_code {meli_code} does not exist."}
                )

        # Save the updated teacher instance
        instance.save()
        return instance


class TeacherNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'body', 'updated_at']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.updated_at = timezone.now()
        instance.save()
        return instance


class StudentNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'body']


class StudentAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'body', 'file', 'delivery_deadline']


class AnsAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ans_assignment
        fields = ['id', 'assignment', 'body', 'file', 'created_at', 'updated_at']

    def validate_file(self, value):
        if value and not value.name.endswith(('.zip', '.pdf')):
            raise serializers.ValidationError('Only ZIP and PDF files are allowed.')
        return value

    def validate(self, data):
        assignment = data.get('assignment')
        if assignment and assignment.delivery_deadline < timezone.now().date():
            raise serializers.ValidationError(
                "The deadline for this assignment has passed. You cannot submit an answer"
            )
        return data

    def create(self, validated_data):
        student = self.context['request'].user

        if validated_data['assignment'].teacher != student.teacher:
            raise serializers.ValidationError("You can only submit answers for your teacher's assignments.")

        if Ans_assignment.objects.filter(student=student, assignment=validated_data['assignment']).exists():
            raise serializers.ValidationError("You have already submitted an answer for this assignment.")

        validated_data['student'] = student
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data['assignment'].delivery_deadline < timezone.now().date():
            raise serializers.ValidationError(
                "The deadline for this assignment has passed. You cannot update the answer")
        else:
            instance.assignment = validated_data['assignment']
            instance.body = validated_data.get('body', instance.body)
            instance.updated_at = timezone.now()
            instance.save()
            return instance


class TeacherAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'body', 'file', 'delivery_deadline', 'updated_at']

    def validate_file(self, request):
        if request is not None:
            if not request.name.endswith(('.zip', '.pdf')):
                raise serializers.ValidationError('Only ZIP and PDF files are allowed.')
        return request

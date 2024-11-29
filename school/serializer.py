from rest_framework import serializers
from account.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


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

    def create(self, validated_data):
        is_teacher = validated_data.pop('is_teacher')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        meli_code = validated_data.pop('meli_code')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')

        if not meli_code.isdigit():
            raise serializers.ValidationError('Meli code must be an integer')
        if is_teacher:
            user = Teacher.objects.create(**validated_data)
        else:
            user = Student.objects.create(**validated_data)
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
        """
        Update and return the existing Teacher instance.
        """
        # Update basic fields for the teacher
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
                instance.students.add(student)  # Add student to teacher's students
            except Student.DoesNotExist:
                raise serializers.ValidationError(
                    {"students_to_add": f"Student with meli_code {meli_code} does not exist."}
                )

        # Remove students based on meli_code
        students_to_remove = validated_data.get('students_to_remove', [])
        for meli_code in students_to_remove:
            try:
                student = Student.objects.get(meli_code=meli_code)
                instance.students.remove(student)  # Remove student from teacher's students
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
        fields = ['id','title', 'body']


class StudentNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'body']

class TeacherAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id','title', 'body', 'file','delivery_deadline']

class StudentAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id','title', 'body', 'file','delivery_deadline']


class AnsAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ans_assignment
        fields = ['id', 'assignment', 'body', 'file', 'created_at', 'updated_at']

    def validate(self, data):
        assignment = data['assignment']
        if assignment.delivery_deadline < timezone.now().date():
            raise serializers.ValidationError("The deadline for this assignment has passed. You cannot submit an answer.")
        return data

    def create(self, validated_data):
        student = self.context['request'].user

        # Validate that the student is allowed to submit answers for this assignment
        if validated_data['assignment'].teacher != student.teacher:
            raise serializers.ValidationError("You can only submit answers for your teacher's assignments.")

        # Check for existing answers
        if Ans_assignment.objects.filter(student=student, assignment=validated_data['assignment']).exists():
            raise serializers.ValidationError("You have already submitted an answer for this assignment.")

        validated_data['student'] = student
        return super().create(validated_data)

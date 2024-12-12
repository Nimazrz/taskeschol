from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import mixins, authentication
from rest_framework import generics
from .serializer import *
from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from django.contrib.auth import logout, login
from rest_framework import viewsets
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from .Permissions import *


# Create your views here.


class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
        return Response(
            {'message': f'You have successfully logged in'},
            status=status.HTTP_200_OK)


# @csrf_exempt
class LogoutAPIView(APIView):
    """
    {
    "X-CSRFToken": "{% csrf_token %}"
    }
    send this as json request for logout
    """

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': f'You have successfully logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You have not logged in'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self): ?????

    def get_object(self):
        return self.request.user


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]


# for delete and edit need to use the id in url
class TeacherNewsListAPIView(ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = TeacherNewsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)

    # save author from request for news
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StudentNewsListAPIView(ListModelMixin, GenericViewSet):
    serializer_class = StudentNewsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        news = News.objects.filter(author=self.request.user.teacher)
        return news


class TeacherAssignmentsAPIView(viewsets.ModelViewSet):
    serializer_class = TeacherAssignmentsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        teacher = self.request.user
        assignments = Assignment.objects.filter(teacher=teacher)
        return assignments

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class StudentAssignmentsAPIView(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentAssignmentsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, username=self.request.user.teacher)
        return Assignment.objects.filter(teacher=teacher)


class AnsAssignmentViewSet(viewsets.ModelViewSet):
    queryset = Ans_assignment.objects.all()
    serializer_class = AnsAssignmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        # Only return the current user's answers
        return Ans_assignment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

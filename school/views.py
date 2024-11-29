from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.http import HttpResponse, Http404
# api
from rest_framework.views import APIView
from rest_framework import mixins, authentication
from rest_framework import generics
from rest_framework.request import Request
from .serializer import *
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from django.contrib.auth import logout, login
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet


# Create your views here.


class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
        return Response({'message': f'You have successfully logged'}, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    # def get_queryset(self): ?????

    def get_object(self):
        return self.request.user


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


# for delete and edit need to use the id in url
class TeacherNewsListAPIView(ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = TeacherNewsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)

    # save author from request for news
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StudentNewsListAPIView(ListModelMixin, GenericViewSet):
    serializer_class = StudentNewsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        news = News.objects.filter(author=self.request.user.teacher)
        return news

class TeacherAssignmentsAPIView(viewsets.ModelViewSet):
    serializer_class = TeacherAssignmentsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        teacher = self.request.user
        assignments = Assignment.objects.filter(teacher=teacher)
        return assignments

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class StudentAssignmentsAPIView(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentAssignmentsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Assignment.objects.filter(teacher=self.request.user.teacher)


class AnsAssignmentViewSet(viewsets.ModelViewSet):
    queryset = Ans_assignment.objects.all()
    serializer_class = AnsAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return the current user's answers
        return Ans_assignment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)














@login_required(login_url='school:login')
def page(request):
    if request.user is None:
        return redirect('school:login')

    if request.user.is_teacher:
        template = 'school/teacher_page.html'
    else:
        template = 'school/student_page.html'

    return render(request, template)


@login_required(login_url='school:login')
def teacher_profile(request, user_id):
    if not request.user.is_teacher:
        return HttpResponseForbidden("شما مجوز لازم برای دسترسی به این صفحه رو ندارید")
    students = Student.objects.filter(teacher_id=user_id)
    context = {
        'students': students
    }
    return render(request, 'school/teacher_profile.html', context)


def student_profile(request, user_id):
    pass


@login_required  # Ensure the user is logged in
def students(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden("شما مجوز لازم برای دسترسی به این صفحه رو ندارید")

    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'school/students.html', context)


@login_required  # Ensure the user is logged in
def add_student(request, st_id):
    try:
        student = get_object_or_404(Student, id=st_id)
        teacher = request.user
    except:
        raise Http404("Student does not exist")
    student.teacher = teacher
    student.save()

    return redirect('school:students')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("school:page")
            else:
                # Add an error message if authentication fails
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def loged_out(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            is_teacher = form.cleaned_data['is_teacher']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            meli_code = form.cleaned_data['meli_code']
            school = form.cleaned_data['school']
            bio = form.cleaned_data['bio']

            hashed_password = make_password(password)  # Hash the password

            if is_teacher:
                teacher = Teacher(username=username, password=hashed_password, first_name=first_name,
                                  last_name=last_name,
                                  meli_code=meli_code, school=school, bio=bio)
                teacher.save()  # Save the teacher object
                return render(request, 'registration/register_done.html', {'teacher': teacher})
            else:
                student = Student(username=username, password=hashed_password, first_name=first_name,
                                  last_name=last_name,
                                  meli_code=meli_code, school=school, bio=bio)
                student.save()  # Save the student object
                return render(request, 'registration/register_done.html', {'student': student})

    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

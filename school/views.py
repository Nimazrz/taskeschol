from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden


from django.http import HttpResponse, JsonResponse, Http404


# from .forms import RegisterForm

# Create your views here.


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

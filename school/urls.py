from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'school'

urlpatterns = [
    path('', views.page, name='page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.loged_out, name='logout'),
    path('register/', views.register, name='register'),
    path('teacher_profile/<int:user_id>', views.teacher_profile, name='teacher_profile'),
    path('student_profile/<int:user_id>', views.student_profile, name='student_profile'),
    path('students/', views.students, name='students'),
    path('add_student/<int:st_id>/', views.add_student, name='add_student'),
]
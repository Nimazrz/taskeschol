from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

app_name = 'school'

router = DefaultRouter()
router.register(r'teacher_news', views.TeacherNewsListAPIView, basename='teacher_news')
router.register(r'news', views.StudentNewsListAPIView, basename='news')
router.register(r'teacher_assignments', views.TeacherAssignmentsAPIView, basename='teacher_assignments')
router.register(r'student_assignments', views.StudentAssignmentsAPIView, basename='student_assignments')
router.register(r'answer', views.AnsAssignmentViewSet, basename='answer')
urlpatterns = [

    path('api/register/', views.RegistrationAPIView.as_view(), name='register_api'),
    path('api/login/', views.LoginAPIView.as_view(), name='login_api'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout_api'),

    #view profile and edit data
    path('api/profile/', views.UserProfileAPIView.as_view(), name='user-profile'),

    path('api/students/', views.StudentListAPIView.as_view(), name='student-list'),

    path('api/', include(router.urls)),

]

from django.contrib import admin
from .models import *


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',)
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_teacher', 'school')
    ordering = ('-created_at',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name','teacher')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_active', )
    ordering = ('-created_at',)
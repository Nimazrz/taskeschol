from django.contrib import admin
from .models import *
from school.models import Assignment, News, Ans_assignment


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',)
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_teacher', 'school')
    ordering = ('-created_at',)
    actions = [AssignmentInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'teacher')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_active',)
    ordering = ('-created_at',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'author')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'delivery_deadline')


@admin.register(Ans_assignment)
class Ans_assignmentAdmin(admin.ModelAdmin):
    list_display = ['student']

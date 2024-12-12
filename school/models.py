from django.db import models
from account.models import Teacher, Student


# Create your models here.

class News(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='assignments/%Y/%m/%d', blank=True, null=True)
    delivery_deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by teacher: {self.teacher}"


class Ans_assignment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='ans_assignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='answer')
    body = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='assignments/%Y/%m/%d', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.assignment} by student: {self.student}"

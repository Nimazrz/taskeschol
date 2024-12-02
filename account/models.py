from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    # this is for useing AbstractBaseUser for custom manager
    # def get_by_natural_key(self, username): 
    #     return self.get(username=username)


class Teacher(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    meli_code = models.CharField(max_length=10)
    school = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    is_teacher = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='teacher_groups',  # Unique related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='teacher_permissions',  # Unique related name
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'meli_code']

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return self.username


class Student(AbstractBaseUser, PermissionsMixin):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    meli_code = models.CharField(max_length=10)
    school = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    is_teacher = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_groups',  # Unique related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_permissions',  # Unique related name
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'meli_code']

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return self.username


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



class Ans_assignment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='ans_assignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='answer')
    body = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='assignments/%Y/%m/%d', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

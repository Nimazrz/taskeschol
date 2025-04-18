# Generated by Django 5.1.3 on 2024-12-12 22:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0012_remove_assignment_teacher_remove_news_author_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField(blank=True, max_length=1000, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='assignments/%Y/%m/%d')),
                ('delivery_deadline', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Ans_assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, max_length=1000, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='assignments/%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ans_assignments', to='account.student')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='school.assignment')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

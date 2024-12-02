# Generated by Django 5.1.3 on 2024-12-02 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_ans_assignment_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ans_assignment',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ans_assignments', to='account.student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='meli_code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='meli_code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-01 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_is_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-21 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electricapp', '0009_alter_attendance_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='address',
            field=models.TextField(default='None'),
        ),
    ]
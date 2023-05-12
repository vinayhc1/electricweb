# Generated by Django 4.1.7 on 2023-04-18 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electricapp', '0007_alter_item_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=1, max_digits=1)),
            ],
        ),
    ]

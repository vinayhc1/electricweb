# Generated by Django 4.1.7 on 2023-04-22 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electricapp', '0011_rename_customers_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=50)),
                ('item', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]

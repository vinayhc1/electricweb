# Generated by Django 4.2 on 2023-05-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electricapp', '0018_matlist_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='matlist',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-15 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electricapp', '0004_rename_items_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('RCC', 'RCC'), ('FITTINGS', 'FITTINGS')], default='RCC', max_length=20),
        ),
    ]
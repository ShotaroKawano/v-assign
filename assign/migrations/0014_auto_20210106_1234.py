# Generated by Django 2.2.17 on 2021-01-06 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assign', '0013_auto_20210106_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(),
        ),
    ]

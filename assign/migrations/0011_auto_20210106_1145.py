# Generated by Django 2.2.17 on 2021-01-06 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assign', '0010_auto_20210106_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworkingtime',
            name='target_day',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dailyworkingtime',
            name='target_month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='monthlyworkingtime',
            name='target_month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.IntegerField(),
        ),
    ]

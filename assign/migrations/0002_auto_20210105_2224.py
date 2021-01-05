# Generated by Django 2.2.17 on 2021-01-05 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assign', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('is_checked', models.BooleanField()),
            ],
        ),
        migrations.DeleteModel(
            name='BoardModel',
        ),
    ]

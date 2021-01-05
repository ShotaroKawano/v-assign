# Generated by Django 2.2.17 on 2021-01-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('good', models.IntegerField()),
                ('read', models.IntegerField()),
                ('readtext', models.CharField(max_length=200)),
            ],
        ),
    ]

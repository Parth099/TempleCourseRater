# Generated by Django 3.0.7 on 2020-10-17 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CourseId', models.CharField(max_length=5)),
                ('Program', models.CharField(max_length=200, null=True)),
                ('CourseName', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]

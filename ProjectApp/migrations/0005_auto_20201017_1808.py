# Generated by Django 3.0.7 on 2020-10-17 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectApp', '0004_auto_20201017_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='CourseId',
            new_name='CourseID',
        ),
    ]

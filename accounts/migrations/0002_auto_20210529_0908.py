# Generated by Django 3.2.3 on 2021-05-29 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='base_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='base_user',
            new_name='user',
        ),
    ]

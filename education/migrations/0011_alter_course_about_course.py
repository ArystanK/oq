# Generated by Django 3.2.3 on 2021-06-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_remove_assignment_is_graded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='about_course',
            field=models.TextField(),
        ),
    ]

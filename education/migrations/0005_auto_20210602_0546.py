# Generated by Django 3.2.3 on 2021-06-02 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20210602_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='is_submitted',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='link',
        ),
    ]
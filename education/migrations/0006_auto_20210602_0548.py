# Generated by Django 3.2.3 on 2021-06-02 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_auto_20210602_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.TextField(default='description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]

# Generated by Django 3.2.3 on 2021-06-02 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210529_1006'),
        ('education', '0006_auto_20210602_0548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='group',
        ),
        migrations.AddField(
            model_name='assignment',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student'),
        ),
    ]
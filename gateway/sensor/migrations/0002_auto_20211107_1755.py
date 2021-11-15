# Generated by Django 3.2.9 on 2021-11-07 23:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensor',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

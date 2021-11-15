# Generated by Django 3.2.9 on 2021-11-13 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_auto_20211107_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actuator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actuator_name', models.CharField(max_length=50, unique=True)),
                ('location', models.CharField(max_length=50)),
                ('actuator_status', models.IntegerField()),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
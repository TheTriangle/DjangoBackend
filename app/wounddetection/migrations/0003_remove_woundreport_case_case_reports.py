# Generated by Django 4.2.7 on 2024-03-10 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wounddetection', '0002_case_doctor_specialization_woundreport_delete_wound_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='woundreport',
            name='case',
        ),
        migrations.AddField(
            model_name='case',
            name='reports',
            field=models.ManyToManyField(to='wounddetection.woundreport'),
        ),
    ]
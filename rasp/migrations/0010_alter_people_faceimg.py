# Generated by Django 4.2.13 on 2024-12-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasp', '0009_alter_people_faceimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='faceImg',
            field=models.FileField(upload_to='all_face'),
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-01 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='assert/answer'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='profilepic',
            field=models.FileField(null=True, upload_to='media/userprofile'),
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-04 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0004_question_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='questiondate',
            new_name='answerdatedate',
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-04 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='commentPost',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='commentUser',
        ),
    ]

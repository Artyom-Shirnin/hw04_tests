# Generated by Django 2.2.19 on 2022-04-30 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20220430_1421'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='text',
            new_name='title',
        ),
    ]

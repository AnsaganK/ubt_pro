# Generated by Django 3.1.7 on 2021-04-04 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0025_auto_20210404_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='lesson',
            new_name='lessons',
        ),
    ]

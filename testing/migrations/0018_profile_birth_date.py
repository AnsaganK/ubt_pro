# Generated by Django 3.1.7 on 2021-03-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0017_question_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

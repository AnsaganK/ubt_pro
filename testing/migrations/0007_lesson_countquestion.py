# Generated by Django 3.1.4 on 2021-03-03 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0006_lesson_basic'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='countQuestion',
            field=models.CharField(choices=[('15', '15'), ('20', '20'), ('35', '35')], default='35', max_length=200),
        ),
    ]

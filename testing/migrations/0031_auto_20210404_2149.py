# Generated by Django 3.1.7 on 2021-04-04 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0030_auto_20210404_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='lessons',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to='testing.Lesson'),
        ),
    ]

# Generated by Django 3.1.7 on 2021-03-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0013_usertests'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertests',
            options={'verbose_name': 'Тест пользователя', 'verbose_name_plural': 'Тесты пользователей'},
        ),
        migrations.AddField(
            model_name='answer',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='answer_img'),
        ),
    ]
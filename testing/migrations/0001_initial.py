# Generated by Django 3.1.7 on 2021-03-02 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Контент')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Контент')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('archive', models.BooleanField(default=False, verbose_name='Архив')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Контент')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
            },
        ),
        migrations.CreateModel(
            name='Tutors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=200, null=True, verbose_name='Отчество')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Эл.почта')),
                ('phone_number', models.TextField(verbose_name='Мобильный телефон')),
                ('birth_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')),
                ('lesson', models.ManyToManyField(related_name='tutors', to='testing.Lesson', verbose_name='Предметы')),
            ],
            options={
                'verbose_name': 'Учитель',
                'verbose_name_plural': 'Учителя',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

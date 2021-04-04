from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


class Pages(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(null=True, blank=True, verbose_name="Контент")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    basic = models.BooleanField(default=False, verbose_name="Главная")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(null=True, blank=True, verbose_name="Контент")
    img = models.FileField(null=True, blank=True, verbose_name="Картинка")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Изменено")
    archive = models.BooleanField(default=False, verbose_name="Архив")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsDetail', args=[str(self.id)])

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    photo = models.FileField(upload_to="LessonPhoto", null=True, blank=True)
    content = models.TextField(null=True, blank=True, verbose_name="Контент")
    basic = models.BooleanField(default=False, verbose_name="Основной предмет")

    countQuestionChoices = (
        ('15', '15'),
        ('20', '20'),
        ('35', '35'),
    )
    countQuestion = models.CharField(max_length=200, default="35", choices=countQuestionChoices)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Tutors(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=200, verbose_name="Имя")
    last_name = models.CharField(null=True, blank=True, max_length=200, verbose_name="Фамилия")
    patronymic = models.CharField(null=True, blank=True, max_length=200, verbose_name="Отчество")
    photo = models.FileField(upload_to="photoTutors", null=True, blank=True, verbose_name="Фотография")
    email = models.EmailField(null=True, blank=True, verbose_name="Эл.почта")
    phone_number = models.TextField(null=True, blank=True, verbose_name="Мобильный телефон")
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождения")

    lesson = models.ManyToManyField(Lesson, null=True, blank=True, related_name="tutors", verbose_name="Предметы")

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    photo = models.FileField(upload_to="photoUsers", null=True, blank=True, verbose_name="Фотография")
    lessons = models.ManyToManyField(Lesson,blank=True, null=True, related_name='users')
    role = models.ForeignKey("Role",null=True, blank=True, on_delete=models.CASCADE, verbose_name="Роль", related_name="users")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Code(models.Model):
    trial = models.BooleanField(default=False)
    number = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('codeLessons', args=[str(self.id)])

    class Meta:
        verbose_name = 'Код'
        verbose_name_plural = 'Коды'


class CodeGroups(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE, related_name="groups")
    users = models.ManyToManyField(User, related_name="codeGroups")
    group = models.ForeignKey("UserGroups", on_delete=models.CASCADE, related_name="codes")
    dateCreate = models.DateTimeField(auto_now_add=True)
    dateUpdate = models.DateTimeField(auto_now=True)

    dateStart = models.DateTimeField(null=True, blank=True)
    dateEnd = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.code.number) + " | " + str(self.group.name)

    class Meta:
        verbose_name = "ЕНТ для групп"
        verbose_name_plural = "ЕНТ для групп"


class Test(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True, default="Без названия",
                            verbose_name='Названия теста')
    questions = models.ManyToManyField('Question')
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="my_tests")
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE, related_name="tests")
    archive = models.BooleanField(default=False)

    code = models.ForeignKey(Code, on_delete=models.CASCADE, null=True, blank=True, related_name="tests",
                             verbose_name="Код теста")

    def get_absolute_url(self):
        return reverse('testTake', args=[str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    text = RichTextUploadingField()
    high = models.BooleanField(default=False)
    img = models.FileField(upload_to="question_img", null=True, blank=True)
    answers = models.ManyToManyField('Answer', related_name='question')
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name='Вариант ответа')
    img = models.FileField(upload_to="answer_img", null=True, blank=True)
    right = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UserTests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="users")
    schema = JSONField(null=True, blank=True)
    result = models.IntegerField(null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " | " + self.test.name

    def get_absolute_url(self):
        return reverse('resultDetail', args=[str(self.id)])

    class Meta:
        ordering = ['-date']
        verbose_name = "Тест пользователя"
        verbose_name_plural = "Тесты пользователей"


class UserGroups(models.Model):
    users = models.ManyToManyField(User, related_name='userGroups', verbose_name='Пользователи')
    name = models.CharField(max_length=50)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('userGroupsDetail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class Role(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
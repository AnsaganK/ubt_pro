from django.urls import path
from .views import *
from django.contrib.auth import views as acc

urlpatterns = [
    path('', about, name="about"),
    path('news', news, name="news"),
    path('newsAdd', newsAdd, name="newsAdd"),
    path('tutors', tutors, name="tutors"),
    path('lessons', lessons, name="lessons"),
    path('lessonAdd', lessonAdd, name="lessonAdd"),
    path('uslugi', uslugi, name="uslugi"),
    path('testSave/<int:pk>', testSave, name="testSave"),
    path('codes', codes, name="codeAdd"),
    path('codesAdd', codesAdd, name="codeAddForm"),
    path('codeLessons/<int:pk>', codeLessons, name="codeLessons"),
    path('lessons/<int:pk>', lessonDetail, name="lessonDetail"),
    path('lesson_delete/<int:pk>', lessonDelete, name="lessonDelete"),
    path('lesson_edit/<int:pk>', lessonEdit, name="lessonEdit"),
    path('exams', entList, name="exams"),
    path('examsCreate', entCreate, name="examsCreate"),
    path('testCreatePage/<int:pk>', testCreatePage, name="testCreatePage"),
    path('testTake/<int:pk>', testTake, name="testTake"),
    path('testResult', testResult, name="testResult"),
    path('testResult/<int:pk>', resultDetail, name="resultDetail"),
    path('test_result_user_list/<int:pk>', testResultUserList, name="testResultUserList"),
    path('news/<int:pk>', newsDetail, name="newsDetail"),
    path('user_list', userList, name="userList"),
    path('roleUsers/<int:pk>', roleUsers, name="roleUsers"),
    path('groups', groups, name="groups"),
    path('groups/<int:pk>', userGroupsDetail, name="userGroupsDetail"),
    path('groupCreate', groupCreate, name="groupCreate"),
    path('testForUser/<int:pk>', testForUser, name="testForUser"),

    path('userCreate', userCreate, name="userCreate"),
    path('profile', profile, name="profile"),
    path('signup', signup, name="signup"),
]
urlpatterns += [
    path('accounts/login/', acc.LoginView.as_view(), name='login'),
    path('accounts/logout/', acc.LogoutView.as_view(), name='logout'),
    path('accounts/password-reset', acc.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-change/done/', acc.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password-change', acc.PasswordChangeView.as_view(), name='password_change'),
]

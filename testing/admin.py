from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import Pages, News, Lesson, Profile, Test, Question, Answer, Code, UserTests, CodeGroups, Role

admin.site.register(News)
admin.site.register(Lesson)
admin.site.register(Profile)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Code)
admin.site.register(CodeGroups)
admin.site.register(UserTests)
admin.site.register(Role)


class PagesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    content_ru = forms.CharField(widget=CKEditorUploadingWidget)
    content_kk = forms.CharField(widget=CKEditorUploadingWidget)
    content_en = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Pages
        fields = "__all__"


class PagesAdmin(admin.ModelAdmin):
    form = PagesAdminForm


admin.site.register(Pages, PagesAdmin)

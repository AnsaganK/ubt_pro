from django import template
import json
import random
register = template.Library()

@register.filter(name="shortContent")
def shortContent(text):
    return text[:150]

@register.filter(name='dateTransform')
def dateTransform(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hour = date.hour+6
    if hour>=24:
        date.hour = date.hour+6-24
    if hour<10:
        hour = "0"+str(hour)
    else:
        hour = str(hour)
    if date.minute<10:
        minute = "0"+str(date.minute)
    else:
        minute = str(date.minute)
    newDate = "{0}:{1}  {2}/{3}/{4}".format(hour, minute, day, month, year)
    return newDate

@register.filter(name='randomAnswers')
def randomAnswers(lst):
    a = list(lst)
    random.shuffle(a)
    #print(a)
    return a

@register.filter(name='isGroup')
def isGroup(user, group):
    if user.profile.role.name_ru == group:
        return True
    return False


@register.filter(name='returnDicEl')
def returnDicEl(data, id):
    return data[id]




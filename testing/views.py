from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect

from .forms import UserForm, LessonForm, NewsForm, UserGroupsForm, ENTForm
from .models import Test, Question, Answer, Lesson, Tutors, Pages, UserTests, News, Code, UserGroups, CodeGroups, Role


def about(request):
    page = Pages.objects.filter(basic=True).first()
    context = {}
    if page:
        context = {"title": page.title, "content": page.content}
    return render(request, "about.html", context)


def page(request, pk):
    p = Pages.objects.get(pk=pk)
    return render(request, "page.html", {"page": p})


def news(request):
    news = News.objects.all()
    return render(request, "news.html", {"news_list": news})


def tutors(request):
    tutors = Tutors.objects.all()
    return render(request, "tutors.html", {"tutors": tutors})


def lessons(request):
    lessons = Lesson.objects.all()
    basicLessons = lessons.filter(basic=True)
    changeLessons = lessons.filter(basic=False)
    return render(request, "lessons.html", {"lessons": changeLessons, "basicLessons": basicLessons})


def uslugi(request):
    return render(request, "uslugi.html")


def testCreatePage(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    codes = Code.objects.exclude(tests__lesson=lesson)
    if lesson.countQuestion == "35":
        easyQuestion = 25
        hardQuestion = 10
    else:
        easyQuestion = int(lesson.countQuestion)
        hardQuestion = 0
    return render(request, "testCreatePage.html", {"easyQuestions": range(1, easyQuestion + 1),
                                                   "hardQuestions": range(easyQuestion + 1,
                                                                          easyQuestion + hardQuestion + 1),
                                                   "name": lesson.title,
                                                   "id": lesson.pk,
                                                   "codes": codes})


def testCreate(questions, pk, codeTest):
    print(codeTest)
    code = Code.objects.get(pk=int(codeTest))
    lesson = Lesson.objects.get(pk=pk)
    test = Test.objects.create(lesson=lesson, code=code)
    for i in questions:
        text = questions[i]["text"]
        high = questions[i]["high"]
        question = Question.objects.create(text=text, high=high)
        for j in questions[i]["answers"]:
            answer = Answer.objects.create(text=j[0], right=j[1], img=j[2])
            # answer.save()
            question.answers.add(answer)
        # question.save()
        test.questions.add(question)
    # test.save()


def testSave(request, pk):
    if request.method == "POST":
        questions = {}
        right_answers_list = []
        img_answers_list = []
        dic = dict(request.POST)
        files = dict(request.FILES)
        print(dic)
        for i in dic:
            if i.split("_")[0] == "question":
                questions["question_{}".format(i.split("_")[1])] = {
                    "text": dic[i][0],
                    "answers": [],
                    "high": True if i.split("_")[-1] == "high" else False}
        for i in dic:
            if i.split("_")[0] == "r":
                right_answers_list.append(dic[i][0])
        for i in dic:
            if i.split("_")[0] == "variant":
                questions[
                    "question_{}".format(i.split("_")[1])]["answers"].append([
                    dic[i][0],
                    True if i.replace("variant_", "") in right_answers_list else False,
                    files["img_{}".format(i.replace("variant_", ""))][0] if "img_{}".format(
                        i.replace("variant_", "")) in files else None
                ])
        print(questions)
        testCreate(questions, pk, dic["codeTest"][0])
    return redirect("/lessons/{}".format(pk))


def lessonDetail(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    return render(request, "tests.html", {"lesson": lesson})


def lessonDelete(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    lesson.delete()
    return redirect('lessons')


def lessonEdit(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
        return redirect('lessons')
    count = Lesson.countQuestionChoices
    return render(request, 'lessonEdit.html', {"lesson": lesson, "count": count})


def testTake(request, pk):
    test = Test.objects.get(pk=pk)
    return render(request, 'testTake.html', {"test": test})


def emailValid(email):
    user = User.objects.filter(email=email)
    if user:
        return True
    return False


def userValid(username):
    try:
        user = User.objects.get(username=username)
        return username
    except:
        return False


def userCreate(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        role = Group.objects.get(pk=request.POST["group"][0])
        userFound = userValid(request.POST["username"])
        emailFound = emailValid(request.POST["email"])
        passwordCheck = request.POST["password1"] != request.POST["password2"]
        if form.is_valid() and not (userFound or emailFound or passwordCheck):
            user = form.save()
            user.profile.role = role
            user.save()
            return redirect("about")
        else:
            # print(form.errors)
            roles = Role.objects.all()
            return render(request, "userCreatePage.html",
                          {"groups": roles, "userFound": userFound, "passwordCheck": passwordCheck,
                           "emailFound": emailFound})
    else:
        role = Role.objects.get(name_ru="Админ")
        if role == request.user.profile.role:
            roles = Role.objects.all()
            return render(request, "userCreatePage.html", {"groups": roles})
        else:
            return render(request, "404.html")


def checkQuestionBall(checkAnswers, rightAnswers, high):
    rights = [i.pk for i in rightAnswers]
    zero = 0
    for i in checkAnswers:
        if int(i) in rights:
            zero += 1
    if high:
        if zero == len(rights) and len(checkAnswers) == zero and len(rights) != 0:
            return 2
        if zero == len(rights) - 1 and len(checkAnswers) == zero and len(rights) > 1:
            return 1
        else:
            return 0
    else:
        if zero == len(rights) and len(rights) != 0:
            return 1
        else:
            return 0


def testResult(request):
    if request.method == "POST":
        balls = 0
        post = dict(request.POST)
        test = Test.objects.get(pk=int(post["testId"][0]))
        jsonSchema = {"questions": []}
        for i in post:
            if i != "tab-btn" and i != "csrfmiddlewaretoken" and i != "testId":
                question = Question.objects.get(pk=int(i))
                answers = question.answers.filter(right=True)
                ball = checkQuestionBall(post[i], answers, high=True if question.high else False)
                balls += ball
                jsonSchema["questions"].append({"questionId": question.id,
                                                "question": question.text,
                                                "answerCheck": [int(j) for j in post[i]],
                                                "answerRight": [j.pk for j in answers],
                                                "ball": ball
                                                })
        a = UserTests.objects.create(user=request.user, test=test, schema=jsonSchema, result=balls)

        return redirect("testResult/{}".format(a.pk))
    return redirect("about")


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form)
        userFound = userValid(request.POST["username"])
        emailFound = emailValid(request.POST["email"])
        passwordCheck = request.POST["password1"] != request.POST["password2"]
        if form.is_valid() and not (userFound or emailFound or passwordCheck):
            user = form.save()
            role = Role.objects.get(name_ru='Админ')
            user.profile.role = role
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("about")
        else:
            return render(request, "registration/signup.html",
                          {"userFound": userFound, "passwordCheck": passwordCheck, "emailFound": emailFound})
    else:
        return render(request, "registration/signup.html")


def profile(request):
    user = request.user
    role = Role.objects.filter(name_ru="Учитель").first()
    if role == user.profile.role:
        lessons = user.profile.lessons.all()
        return render(request, "profileForTeacher.html", {"teacher": True, "lessons": lessons})
    return render(request, "profile.html")


def lessonAdd(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lessons')
        return render(request, "profile.html")
    count = Lesson.countQuestionChoices
    return render(request, "lessonAdd.html", {"count": count})


def testResultUserList(request, pk):
    tests = UserTests.objects.filter(test_id=pk)
    # print(tests)
    return render(request, "test_result_user_list.html", {"tests": tests})


def resultDetail(request, pk):
    test = UserTests.objects.get(pk=pk)
    json = test.schema
    data = json["questions"]
    # print(data)
    # print()
    for i in data:
        i["answerCheckIn"] = []
        i["answerRightIn"] = []
        for j in i["answerCheck"]:
            answer = Answer.objects.get(pk=j)
            i["answerCheckIn"].append({"text": answer.text, "image": answer.img.url if answer.img else None,
                                       "isRight": True if answer.pk in i["answerRight"] else False})
            # print(i["answerCheck"])
        for j in i["answerRight"]:
            answer = Answer.objects.get(pk=j)
            i["answerRightIn"].append({"text": answer.text, "image": answer.img.url if answer.img else None})
    # print(data)
    return render(request, 'resultDetail.html', {"test": test})


def newsDetail(request, pk):
    news_item = News.objects.get(pk=pk)
    return render(request, 'newsDetail.html', {"news": news_item})


def newsAdd(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('news')
    return render(request, 'newsAdd.html')


def userList(request):
    roles = Role.objects.all()
    users = User.objects.order_by('-date_joined').all()
    return render(request, "userList.html", {"users": users, "roles": roles})


def testForUser(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'testForUser.html', {'user': user})


def codes(request):
    codes = Code.objects.all()
    return render(request, 'codeAdd.html', {"codes": codes})


def codesAdd(request):
    if request.method == "POST":
        for i in Code.objects.all():
            if i.number == request.POST["code"]:
                return redirect('codeAdd')
        code = Code.objects.create(number=request.POST["code"])
        code.save()
        return redirect('codeAdd')


def codeLessons(request, pk):
    code = Code.objects.get(pk=pk)
    basicLessons = Test.objects.filter(code=code).filter(lesson__basic=True).all()
    changeLessons = Test.objects.filter(code=code).exclude(lesson__basic=True).all()
    # notSelectLessons = Test.objects.filter(code=code).all()
    notSelectLessons = Lesson.objects.exclude(tests__code=code).all()
    # basicLessons = Lesson.objects.filter(basic=True).filter(tests__code__in=code).all()
    # lessons = Lesson.objects.exclude(basic=True).filter(tests__code__in=code).all()
    # notSelectLessons = Lesson.objects.exclude(tests__code__in=code)
    return render(request, 'codeLessons.html',
                  {"basicLessons": basicLessons, "changeLessons": changeLessons, "notSelectLessons": notSelectLessons, "code": code})


def groups(request):
    groups = UserGroups.objects.all()
    return render(request, 'groups.html', {'groups': groups})


def userGroupsDetail(request, pk):
    userGroup = UserGroups.objects.get(pk=pk)
    users = User.objects.all()
    return render(request, 'userGroupsDetail.html', {"group": userGroup, "users": users})


def groupCreate(request):
    if request.method == "POST":
        form = UserGroupsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups')

    groups = UserGroups.objects.all()
    return render(request, 'groups.html', {'groups': groups})


def entList(request):
    user = request.user
    roleAdmin = Role.objects.filter(name_ru="Админ").first()
    if roleAdmin == user.profile.role:
        codes = Code.objects.all()
        userGroups = UserGroups.objects.all()
        ents = CodeGroups.objects.all()
        return render(request, 'entList.html', {"ents": ents, "admin": True, "codes": codes, "userGroups": userGroups})
    role = Role.objects.filter(name_ru="Гость").first()
    if user.is_authenticated and role != user.profile.role:
        group = user.userGroups.all().first()
        ents = CodeGroups.objects.filter(group=group)
    else:
        ents = Code.objects.filter(trial=True)
    return render(request, 'entList.html', {"ents": ents})


def entCreate(request):
     if request.method == "POST":
        form = ENTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exams')
        else:
            print(form.errors)
     return redirect('exams')


def roleUsers(request, pk):
    role = Role.objects.get(pk=pk)
    users = role.users.all()
    return render(request, "roleUsers.html", {"title": role.name, "users": users})

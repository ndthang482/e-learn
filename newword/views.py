from hashlib import new
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Test, Lesson, NewWord, Quest
import random
from django.core import serializers
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.urls import reverse

# Create your views here.

@login_required
def home(request):
  lessons = Lesson.objects.all()
  context = {
    "lessons": lessons,
  }
  return render(request, "home.html", context)

@login_required
def lesson_test(request, lesson_number):
  newWords = list(NewWord.objects.filter(lesson__number=lesson_number))
  
  test = Test()
  test.user = request.user
  test.lesson = Lesson.objects.filter(number=lesson_number).first()
  test.num_of_quest = len(newWords)
  test.save()
  
  random.shuffle(newWords)
  questions = []
  for newWord in newWords:
    quest = Quest()
    quest_str, result = "", ""
    r = random.randint(1,3)
    if newWord.wtype == 5:
      r = 3
    if r == 1:
      quest_str = f"{newWord.meaning.capitalize()}({newWord.get_wtype_display().lower()}) in English."
      result = newWord.word
    elif r == 2:
      quest_str = f"{newWord.word.capitalize()}({newWord.meaning.lower()}) word type."
      result = str(newWord.wtype)
    elif r == 3:
      quest_str = f"{newWord.word.capitalize()}({newWord.get_wtype_display().lower()}) meaning."
      result = newWord.meaning
    quest.question = quest_str
    quest.qtype = r
    quest.test = test
    quest.result = result
    quest.save()
    questions.append(quest)
  request.session["questpks"] = [x.pk for x in questions]
  context = {
    "test": test,
    "questions": questions,
  }
  return render(request, "test.html", context)

@login_required
def grading(request):
  if request.is_ajax and request.method == "POST":
    answer = request.POST.getlist("ans[]")
    questpks = request.session["questpks"]
    for ind, pk in enumerate(questpks):
      quest = Quest.objects.get(pk=pk)
      quest.answer = answer[ind]
      quest.correct = 0
      if answer[ind].lower() == quest.result.lower():
        quest.correct = 1
      quest.save()
    test = quest.test
    test.score = Quest.objects.filter(test=test).filter(correct=1).count()
    test.save()
    ser_instance = serializers.serialize('json', [ test, ])
    return JsonResponse({"test": ser_instance}, status=200)
  return JsonResponse({"error": ""}, status=400)

@login_required
def review(request, test_id):
  wtype = {
    "1": "Noun",
    "2": "Verb",
    "3": "Adjective",
    "4": "Adverb"
  }
  test = Test.objects.get(pk=test_id)
  quests = Quest.objects.filter(test=test)
  for quest in quests:
    if quest.result in wtype.keys():
      quest.result = wtype[quest.result]
    if quest.answer in wtype.keys():
      quest.answer = wtype[quest.answer]
  context = {
    "test": test,
    "quests": quests,
    
  }
  return render(request, "review.html", context)

@login_required
def view_history(request):
  tests = Test.objects.filter(user=request.user)
  context = {
    "tests": tests,
  }
  return render(request, "history.html", context)

@user_passes_test(lambda u: u.is_superuser)
def view_history_admin(request):
  tests = Test.objects.all()
  context = {
    "tests": tests,
  }
  return render(request, "history.html", context)

def register(request):
  if request.method == "GET":
    form = CustomUserCreationForm()
    context = {
      "form": form,
    }
    return render(request, "register.html", context)
  elif request.method == "POST":
    form = CustomUserCreationForm(request.POST)
    if form.is_valid:
      user = form.save()
      login(request, user)
      return redirect(reverse("home"))
    else:
      return redirect(reverse("register"))

@login_required
def random_test(request, quest_num):
  test = Test()
  test.user = request.user
  test.num_of_quest = quest_num
  test.save()
  
  allWords = list(NewWord.objects.all())
  wordCount = len(allWords)
  newWordInds, newWords, questions = [], [], []
  index = 0
  while index < test.num_of_quest:
    r = random.randint(1, wordCount-1)
    if r not in newWordInds:
      newWordInds.append(r)
      index += 1
  for pk in newWordInds:
    newWords.append(allWords[pk])
  for newWord in newWords:
    quest = Quest()
    quest_str, result = "", ""
    r = random.randint(1,3)
    if newWord.wtype == 5:
      r = 3
    if r == 1:
      quest_str = f"{newWord.meaning.capitalize()}({newWord.get_wtype_display().lower()}) in English."
      result = newWord.word
    elif r == 2:
      quest_str = f"{newWord.word.capitalize()}({newWord.meaning.lower()}) word type."
      result = str(newWord.wtype)
    elif r == 3:
      quest_str = f"{newWord.word.capitalize()}({newWord.get_wtype_display().lower()}) meaning."
      result = newWord.meaning
    quest.question = quest_str
    quest.qtype = r
    quest.test = test
    quest.result = result
    quest.save()
    questions.append(quest)
  request.session["questpks"] = [x.pk for x in questions]
  context = {
    "test": test,
    "questions": questions,
  }
  return render(request, "test.html", context)

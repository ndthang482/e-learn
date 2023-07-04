from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lesson(models.Model):
  number = models.IntegerField()
  def __str__(self):
      return f"Lesson {self.number}"

class Test(models.Model):
  test_time = models.DateTimeField(auto_now_add=True)
  score = models.IntegerField(null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
  num_of_quest = models.IntegerField(blank=True, null=True)
  def __str__(self):
    return f"Test {self.pk} {self.user}"

class NewWord(models.Model):
  word_type = [
    (1, "Noun"),
    (2, "Verb"),
    (3, "Adjective"),
    (4, "Adverb"),
    (5, "Phrasal verb/Preposition")
  ]
  word = models.CharField(max_length=100)
  wtype = models.IntegerField(choices=word_type, default=1)
  meaning = models.CharField(max_length=100)
  lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name="words")
  def __str__(self):
    return f"{self.word} in {self.lesson}" 

class Quest(models.Model):
  quest_type = [
    (1, "Word fill"),
    (2, "Type choose"),
    (3, "Word meaning")
  ]
  result_type = [
    (0, "False"),
    (1, "True")
  ]
  question = models.CharField(max_length=500)
  result = models.CharField(max_length=150)
  qtype = models.IntegerField(choices=quest_type, default=1)
  answer = models.CharField(max_length=150, blank=True, null=True)
  correct = models.IntegerField(choices=result_type, blank=True, null=True)
  test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="user_answers")
  def __str__(self):
    return f"Quest {self.question}"
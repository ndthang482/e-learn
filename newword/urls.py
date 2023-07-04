from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("lesson_test/<int:lesson_number>", views.lesson_test, name="lesson_test"),
  path("grading/", views.grading, name="grading"),
  path("review/<int:test_id>", views.review, name="review"),
  path("history/", views.view_history, name="history"),
  path("admin_history/", views.view_history_admin, name="admin_history"),
  path("register/", views.register, name="register"),
  path("random_test/<int:quest_num>", views.random_test, name="random_test"),
]
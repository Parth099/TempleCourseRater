from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:dept>/<str:Id>', views.CoursePage, name='CoursePage')
]
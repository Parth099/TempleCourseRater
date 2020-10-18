from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search/<str:query>', views.searchCourses, name= 'Search'), 
    path('<str:dept>/<str:Id>', views.CoursePage, name='CoursePage'),

]
import django_filters
from django.forms.widgets import Input

from .models import *

class CourseFilter(django_filters.FilterSet):
    Program = django_filters.CharFilter(lookup_expr='icontains', 
                                        label='Program', 
                                        widget = Input(attrs={'placeholder':'Ex: Chem',}) 
                                        )

    CourseID = django_filters.CharFilter(
                                        label='Course Number', 
                                        widget = Input(attrs={'placeholder':'4 Digit Number', 'class': "form-control",}) 
                                        )
    class Meta:
        model = Course
        fields = ["CourseID", "Program", ]
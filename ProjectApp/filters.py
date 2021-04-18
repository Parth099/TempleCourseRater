import django_filters
from django.forms.widgets import Input

from .models import *

class CourseFilter(django_filters.FilterSet):
    Program = django_filters.CharFilter(lookup_expr='icontains', 
                                        label='Program', 
                                        widget = Input(attrs={'placeholder':'Ex: Chem',}) 
                                        )

    ProgramAPPX = django_filters.CharFilter(
                                        lookup_expr='icontains', 
                                        field_name="Program",
                                        label='Program', 
                                        widget = Input(attrs={'placeholder':'Ex: Chem',}) 
                                        )


    CourseID = django_filters.CharFilter(
                                        label='Course Number', 
                                        widget = Input(attrs={'placeholder':'4 Digit Number', 'class': "form-control",}) 
                                        )

    CourseNumA = django_filters.NumberFilter(
                                        field_name="CourseNum",
                                        label='CourseNum Min', 
                                        widget = Input(attrs={'placeholder':'Starting Range', 'class': "form-control",}),
                                        lookup_expr="gt",
                                        )
    CourseNumB = django_filters.NumberFilter(
                                        field_name="CourseNum",
                                        label='CourseNum Max', 
                                        widget = Input(attrs={'placeholder':'Starting Range', 'class': "form-control",}),
                                        lookup_expr="lt",
                                        )

    class Meta:
        model = Course
        fields = ["CourseID", "Program", "CourseNum"]

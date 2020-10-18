from django.forms import ModelForm
from .models import *


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('CourseID', 'Program',)

class CommentForm(ModelForm):
    
    class Meta:
        model = Comments
        fields = '__all__'
        widgets = {
          'comment': forms.Textarea(attrs={'rows':10, 'cols':10}),
        }
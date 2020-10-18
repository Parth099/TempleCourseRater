from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

class Course(models.Model):
    CourseID = models.CharField(max_length=5, blank=True)
    Program = models.CharField(max_length=200, null=True, blank=True)
    CourseName =  models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.CourseName


class Comments(models.Model):
    comment = models.TextField()#widget=forms.Textarea(attrs={'rows':'5', 'cols': '5'}))
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    rating= models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(5)])
    date_created = models.DateTimeField(auto_now_add=True, null=True) 

    def __str__(self):
        return self.comment#self.date_created.strftime("%I:%M")
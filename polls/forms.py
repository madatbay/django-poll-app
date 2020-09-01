from django.forms import ModelForm
from django import forms
from .models import Question, Choice

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text','describtion']
        widgets = {
            'question_text': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter name for poll','id':'title'}),
            'describtion': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter name for poll','id':'describtion'})
        }

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields= ['choice_text']
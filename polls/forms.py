from django.forms import ModelForm
from django import forms
from .models import Question, Choice

class AddPoll(ModelForm):
    choice1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter choice'})
    )
    choice2 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter choice'})
    )
    
    class Meta:
        model = Question
        fields = ['question_text','describtion','choice1','choice2']
        widgets = {
            'question_text': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter name for poll','id':'title'}),
            'describtion': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter name for poll','id':'describtion'})
        }

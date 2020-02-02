from django import forms
from django.forms import ModelForm



class TaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Task title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Task desscription'}))
    spent_time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'How much time you spent'}))

    class Meta:
        fields = ['title', 'description', 'spent_time']


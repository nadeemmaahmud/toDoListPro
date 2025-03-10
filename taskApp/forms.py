from django import forms
from . models import Task, Category

class TaskCreateEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'category', 'deadline']

        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CategoryCreateEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
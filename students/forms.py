from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'phone',
            'course',
            'age',
            'address',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter student name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email'
            }),

            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter phone number'
            }),

            'course': forms.TextInput(attrs={
                'placeholder': 'Enter course'
            }),

            'age': forms.NumberInput(attrs={
                'placeholder': 'Enter age'
            }),

            'address': forms.Textarea(attrs={
                'placeholder': 'Enter address',
                'rows': 4
            }),
        }
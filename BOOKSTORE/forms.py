from django import forms
from .models import book


class bookForm(forms.ModelForm):
    class Meta:

        model = book
        widgets = {
            'name': forms.TextInput(attrs={
            'autocomplete': 'off', 
            'autofocus': 'on', 
            'class': 'form-control', 
            'placeholder': 'Enter Name'
            }),
            'bookname': forms.TextInput(attrs={
            'autocomplete': 'off', 
            'autofocus': 'on', 
            'class': 'form-control', 
            'placeholder': 'Enter Name of the Book'
            }), 
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'autocomplete': 'off', 
                'placeholder': 'Enter Short Summary of the Book', 
                'rows': 3, 
            }), 
            'email_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'autocomplete': 'off', 
                'placeholder': 'name@example.com', 
                'width': '200px', 
            }), 
        }
        fields = [
            'name',
            'bookname', 
            'description', 
            'email_id', 
            'picture', 
        ]
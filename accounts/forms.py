from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        initial=User.Role.STUDENT,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    
    # Extra fields for quick profile setup
    university_or_company = forms.CharField(max_length=150, required=False, label="University or Company")
    headline_or_title = forms.CharField(max_length=150, required=False, label="Degree / Designation")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'RadioSelect':
                field.widget.attrs.update({'class': 'form-control'})

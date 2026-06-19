from django import forms
from .models import CustomUser, Application

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Пароль")
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'fio', 'birth_date', 'phone', 'email']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['transport_type', 'start_date', 'payment_method']
        widgets = {
            
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'transport_type': forms.Select(), 
            'payment_method': forms.Select(),
        }
from django import  forms
from .models import Lead ,User
from django.contrib.auth.forms import UserCreationForm
class LeadForm(forms.ModelForm):
    class Meta:
        model =Lead
        fields ='__all__'
        exclude=['profile_picture','special_files','source',' agent']        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
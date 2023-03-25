from django import  forms
from django.urls import reverse
from .models import Agent, Lead ,User
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
    



class AssignForm(forms.Form):
     
    agent =  forms.ModelChoiceField(queryset=Agent.objects.none()) 
    def __init__(self,*args,**kwargs):
        request=kwargs.pop("request")
        agents=Agent.objects.filter(oraganisation=request.user.userprofile)
        super(AssignForm, self).__init__(*args,**kwargs)
        self.fields["agent"].queryset=agents

   
   
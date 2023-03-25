from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse ,reverse_lazy
from .models import Lead ,User ,UserProfile,Category
from .forms import LeadForm,CustomUserCreationForm,AssignForm
from django.views.generic import ListView, DetailView ,DeleteView,CreateView ,UpdateView ,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from agents.mixins import OrgansisorAndLoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
  # Create your views here.

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')
    model = User


def home_page(request):
    return render(request,'home.html')

class LeadListView(LoginRequiredMixin,ListView):
    template_name='lead_list.html'
    queryset=Lead.objects.all()
    context_object_name='leads'
    '''''
    #i do this code to filter the list by agent
    def get_queryset(self):
        # Get the currently logged-in agent
        agent = self.request.user.agent

        # Filter the leads by the current agent
        queryset = Lead.objects.filter(agent=agent)

        return queryset    
    '''''
    # intial queryset of leads for the entire oraganisation
    def get_queryset(self) :
        user=self.request.user
        if user.is_oraganisor:
            queryset = Lead.objects.filter(oraganisation=user.userprofile,agent__isnull=False)
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation,agent__isnull=False)
            #filter for the agent that logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset
    def get_context_data(self, **kwargs) :
        context= super(LeadListView,self).get_context_data(**kwargs)
        user=self.request.user

        if user.is_oraganisor:
            queryset = Lead.objects.filter(oraganisation=user.userprofile,
            agent__isnull=True)

            context.update({
                "unassigned_leads":queryset
            })

        return context    

    
 
class LeadDetailView(OrgansisorAndLoginRequiredMixin,DetailView):
    template_name='lead_detail.html'
    context_object_name='leads'

    def get_queryset(self) :
        user=self.request.user
        if user.is_oraganisor:
            queryset = Lead.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation)
            #filter for the agent that logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrgansisorAndLoginRequiredMixin,CreateView):
    template_name='lead_create.html'
    form_class= LeadForm
    def get_success_url(self):
        return reverse('leads:lead')
    def form_valid(self, form):
        """Send email"""
        send_mail(
            subject="A lead has been created",
            message="Go to the site ",
            from_email="test@test.com",
            recipient_list=["kkamen24@gmail.com"]
        )
        return super(LeadCreateView,self).form_valid(form)
 
    
class LeadUpdateView(OrgansisorAndLoginRequiredMixin,UpdateView):
    template_name='lead_update.html'
    form_class=LeadForm
    context_object_name='leads'
    def get_success_url(self) :
        return reverse('leads:lead_detail',args=[self.object.pk])
    def get_queryset(self) :
        user=self.request.user
        return Lead.objects.filter(oraganisation=user.userprofile)
 
class LeadDeleteView(OrgansisorAndLoginRequiredMixin,DeleteView):
    tempalte_name="lead_delete.html"
    def get_success_url(self):
        return reverse("leads:lead")
    def get_queryset(self) :
        user=self.request.user
        return Lead.objects.filter(oraganisation=user.userprofile)
 

#create a signal
def post_user_created_signla(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

     

post_save.connect(post_user_created_signla,sender=User)




class AssignAgentView(OrgansisorAndLoginRequiredMixin,FormView):
    template_name="assign_agent.html"
    form_class=AssignForm

    def get_success_url(self):
        return reverse("leads:lead")
    
    def get_form_kwargs(self,**kwargs):
        kwargs= super(AssignAgentView,self).get_form_kwargs(**kwargs)

        kwargs.update( {
            "request":self.request,
        })
        return kwargs
    def form_valid(self,form):
        agent=form.cleaned_data["agent"]
        lead=Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)

class CategoryListView(LoginRequiredMixin,ListView):

    template_name="category_list.html"     
    context_object_name="category_list" 

    def get_context_data(self, **kwargs):
        
        user=self.request.user

        context= super(CategoryListView,self).get_context_data(**kwargs)
        if user.is_oraganisor:
            queryset = Lead.objects.filter(oraganisation=user.userprofile )
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation)
        context.update({
             "unassigned_lead_count":queryset.filter(category__isnull=True).count()
        })
        return context
    def get_queryset(self) :
        user=self.request.user
        if user.is_oraganisor:
            queryset = Category.objects.filter(oraganisation=user.userprofile )
        else:
            queryset = Category.objects.filter(oraganisation=user.agent.oraganisation)
             
        return queryset
class CategoryDetailView(LoginRequiredMixin,DetailView):
    template_name="category_detail.html"
    context_object_name="category" 
    def get_context_data(self, **kwargs):
        
        user=self.request.user

        context= super(CategoryDetailView,self).get_context_data(**kwargs)
        leads=self.get_object().leads.all()
        context.update({
             "leads":leads
        })
        return context
    def get_queryset(self) :
        user=self.request.user
        if user.is_oraganisor:
            queryset = Category.objects.filter(oraganisation=user.userprofile )
        else:
            queryset = Category.objects.filter(oraganisation=user.agent.oraganisation)
             
        return queryset
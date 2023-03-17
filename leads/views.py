from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse ,reverse_lazy
from .models import Lead ,User ,UserProfile
from .forms import LeadForm,CustomUserCreationForm
from django.views.generic import ListView, DetailView ,DeleteView,CreateView ,UpdateView
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
            queryset = Lead.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation)
            #filter for the agent that logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset
def lead_list(request):
    leads = Lead.objects.all()
    context ={
        'leads':leads,

    }
    
    return render(request , 'lead_list.html',context)
 
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

def lead_detail(request,pk):
    lead= Lead.objects.get(id=pk)
    context={
        'leads':lead,}
    return render(request,'lead_detail.html',context)
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
def lead_create(request ):
    form =LeadForm()
    if request.method=='POST':
        form=LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
        else:
            form =LeadForm()


    context={
        'form':form
    }
    
    return render(request,'lead_create.html',context )
class LeadUpdateView(OrgansisorAndLoginRequiredMixin,UpdateView):
    template_name='lead_update.html'
    form_class=LeadForm
    context_object_name='leads'
    def get_success_url(self) :
        return reverse('leads:lead_detail',args=[self.object.pk])
    def get_queryset(self) :
        user=self.request.user
        return Lead.objects.filter(oraganisation=user.userprofile)
def lead_update(request, pk):
     

    lead=Lead.objects.get(id=pk)
    form1 =LeadForm(instance=lead)

    if request.method=='POST':
        form1=LeadForm(request.POST,instance=lead)

        if form1.is_valid():
            
            form1.save()
            return redirect(reverse('leads:lead_detail', args=[pk]))

        else:
           
            form1=LeadForm()        
    context={
        'form1':form1,
        'leads':lead
    }
    return render(request,'lead_update.html',context)
#i didnt create delete class because  i prefer being without template 
class LeadDeleteView(OrgansisorAndLoginRequiredMixin,DeleteView):
    tempalte_name="lead_delete.html"
    def get_success_url(self):
        return reverse("leads:lead")
    def get_queryset(self) :
        user=self.request.user
        return Lead.objects.filter(oraganisation=user.userprofile)
def lead_delete(request, pk):

    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')
    

#create a signal
def post_user_created_signla(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

     

post_save.connect(post_user_created_signla,sender=User)
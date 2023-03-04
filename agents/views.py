from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent , UserProfile
from .forms import AgentModelForm



#user = request.user
#user_profile = UserProfile.objects.create(user=user)

class AgentListView(LoginRequiredMixin,generic.ListView):
    template_name="agent_list.html"
    def get_queryset(self):
        return Agent.objects.all()
class AgentDetailView(LoginRequiredMixin,generic.DetailView):
    template_name='agent_detail.html' 
    context_object_name='agent'
    def get_queryset(self):
        return Agent.objects.all()
    
class AgentUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name='agent_update.html'
    form_class= AgentModelForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()  # or create a new form instance
        context['my_form'] = form
        return context
    def get_success_url(self) :
        return reverse("agents:agent_list")
class AgentCreateView(LoginRequiredMixin,generic.CreateView):
    template_name='agent_create.html'
    form_class = AgentModelForm 

    def get_success_url(self) :
        return reverse("agents:agent_list")
    
    def form_valid(self,form):
        try:
            agent=form.save(commit=False)
            agent.oraganisation =self.request.user.userprofile
            agent.save()
            return super(AgentCreateView , self).form_valid(form)
        except:
            return print('This agent does not have a userprofie') and reverse('agents:agent_create')

from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Lead
from .forms import LeadForm
from django.views.generic import ListView, DetailView ,DeleteView,CreateView ,UpdateView
# Create your views here.
def home_page(request):
    return render(request,'home.html')

class LeadListView(ListView):
    template_name='lead_list.html'
    queryset=Lead.objects.all()
    context_object_name='leads'

 
def lead_list(request):
    leads = Lead.objects.all()
    context ={
        'leads':leads,

    }
    return render(request , 'lead_list.html',context)
 
class LeadDetailView(DetailView):
    template_name='lead_detail.html'
    queryset=Lead.objects.all()
    context_object_name='leads'

def lead_detail(request,pk):
    lead= Lead.objects.get(id=pk)
    context={
        'leads':lead,}
    return render(request,'lead_detail.html',context)
class LeadCreateView(CreateView):
    template_name='lead_create.html'
    form_class= LeadForm
    def get_success_url(self):
        return reverse('leads:lead')
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
class LeadUpdateView(UpdateView):
    template_name='lead_update.html'
    queryset=Lead.objects.all()
    form_class=LeadForm
    context_object_name='leads'
    def get_success_url(self) :
        return reverse('leads:lead_detail',args=[self.object.pk])

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
def lead_delete(request, pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Lead
from .forms import LeadForm
# Create your views here.
def home_page(request):
    return render(request,'home.html')

def lead_list(request):
    leads = Lead.objects.all()
    context ={
        'leads':leads,

    }
    return render(request , 'lead_list.html',context)


def lead_detail(request,pk):
    lead= Lead.objects.get(id=pk)
    context={
        'leads':lead,}
    return render(request,'lead_detail.html',context)

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

def lead_delete(request, pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')
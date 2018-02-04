from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Person, Customer, Analyst, Administrator
# Create your views here.

def persons(request):
    emps = Person.objects.all().order_by('user__last_name')
    #print(emps)
    return render(request, 'persons/persons.html', {'emps':emps})

class AddPersons(CreateView):
    model = Person
    fields = ['user','department','positionAtWork','workSince','dismissed']
    success_url="/persons/"
    #print(emps)
    #return render(request, 'persons/persons.html', {'emps':emps})
def customers(request):
    emps = Customer.objects.all().order_by('person__user__last_name')
    #print(emps)
    return render(request, 'persons/customers.html', {'emps':emps})

class AddCustomer(CreateView):
    model = Customer
    fields = ['person','AddBy']
    success_url="/persons/c/"

def analysts(request):
    emps = Analyst.objects.all().order_by('person__user__last_name')
    #print(emps)
    return render(request, 'persons/analysts.html', {'emps':emps})

class AddAnalyst(CreateView):
    model = Analyst
    fields = ['person','AddBy','isHead']
    success_url="/persons/a/"

def administrators(request):
    emps = Administrator.objects.all()
    #print(emps)
    return render(request, 'persons/administrators.html', {'emps':emps})

class AddAdministrator(CreateView):
    model = Administrator
    fields = ['person','AddBy']
    success_url="/persons/x/"


#class PersonCreateView(CreateView):
#    model = Person
#    form_class = FORM_CLASS
#    success_url = 'SUCCESS_URL'
#    template_name = 'TEMPLATE_NAME'

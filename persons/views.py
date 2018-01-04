from django.shortcuts import render
from .models import Person
# Create your views here.

def persons(request):
    emps = Person.objects.all()
    #print(emps)
    return render(request, 'persons/persons.html', {'emps':emps})


class PersonCreateView(CreateView):
    model = Person
    form_class = FORM_CLASS
    success_url = 'SUCCESS_URL'
    template_name = 'TEMPLATE_NAME'

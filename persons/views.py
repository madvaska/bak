from django.shortcuts import render
from .models import Person
# Create your views here.

def persons(request):
    emps = Person.objects.all()
    return render(request, 'persons/persons.html', {'emp':emps})

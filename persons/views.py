from django.shortcuts import render
from .models import Person
# Create your views here.

def persons(request):
    return render(request, 'persons/persons.html', {})

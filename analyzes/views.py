from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze
from persons.models import Customer
from django.views.generic.edit import CreateView


# Create your views here.
def orders(request):
    orders = Order.objects.all()
    #print(emps)
    return render(request, 'analyzes/orders.html', {'orders':orders})


class AddOrder(CreateView):
    model = Order
    fields = ['dateTime','code','codeOfSample','type','customer','project','comment','executed']
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})

def analyzeType(request):
    analyzeTypes = AnalyzeType.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzetypes.html', {'analyzeTypes':analyzeTypes})

class AddAnalyzeType(CreateView):
    model = AnalyzeType
    fields = ['name']
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})

def projects(request):
    projects = Project.objects.all()
    #print(emps)
    return render(request, 'analyzes/projects.html', {'projects':projects})

class AddProject(CreateView):
    model = Project
    fields = ['name']
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})

def analyzes(request):
    analyzes = Analyze.objects.all()
    #print(emps)
    return render(request, 'analyzes/projects.html', {'analyzes':analyzes})

class AddAnalyze(CreateView):
    model = Analyze
    fields = ['dateTime']
    # Создается на основании заявки
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})


#    url(r'^at/$', views.analyzeType, name='Типы анализов'),
#    url(r'^at/add', AddAnalyzeType.as_view(), name='Добавить новый тип анализов'),
#    url(r'^pr/$', views.projects, name='Проекты'),
#    url(r'^pr/add', AddProject.as_view(), name='Добавить новый проект'),

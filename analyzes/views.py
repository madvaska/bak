from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze
from persons.models import Customer,Person
from django.views.generic.edit import CreateView


# Create your views here.
def orders(request):
    types = AnalyzeType.objects.all()
    projects = Project.objects.all()
    customers = Customer.objects.all()
    print(request.POST)
    typeselected = ""
    customerselected = ''
    projectselected = ''
    if request.POST.get('but1', default=None) is None:
        orders = Order.objects.all()
    else:
        str1 = ''
        orders = Order.objects.all()
        typeselected = request.POST.get('type', default=None)
        if typeselected is None:
            pass
        else:
            if typeselected != '0':
                type1 = AnalyzeType.objects.get(name__exact=typeselected)
                orders = orders.filter(type__exact=type1)
        customerselected = request.POST.get('customer', default=None)
        if customerselected is None:
            pass
        else:
            if customerselected != '0':
                person1 = Person.objects.get(lastName__exact=customerselected)
                customer1 = Customer.objects.get(person__exact=person1)
                orders = orders.filter(customer__exact=customer1)

        projectselected = request.POST.get('project', default=None)
        if projectselected is None:
            pass
        else:
            if projectselected != '0':
                project1 = Project.objects.get(name__exact=projectselected)
                orders = orders.filter(project__exact=project1)
            pass
        if request.POST.get('executed', default=None) is None:
            pass

    if typeselected is None:
        typeselected = ''
    if customerselected is None:
        customerselected = ''
    if projectselected is None:
        projectselected = ''
    print("dd="+customerselected)
    return render(request, 'analyzes/orders.html', {'orders':orders, 'types':types,'customers':customers,
    'projects':projects,'typeselected':typeselected,'customerselected':customerselected,'projectselected':projectselected})


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

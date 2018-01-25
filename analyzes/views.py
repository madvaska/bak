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
    if request.POST.get('but1', default=None) is None:
        orders = Order.objects.all()
    else:
        str1 = ''
        orders = Order.objects.all()

        if request.POST.get('type', default=None) is None:
            pass
        else:

            if request.POST.get('type', default=None) != '0':
                print(request.POST.get('type', default=None))
                type1 = AnalyzeType.objects.get(name__exact=request.POST.get('type', default=None))
                orders = orders.filter(type__exact=type1)
        if request.POST.get('customer', default=None) is None:
            pass
        else:
            if request.POST.get('customer', default=None) != '0':
                print(request.POST.get('customer', default=None))
                person1 = Person.objects.get(lastName__exact=request.POST.get('customer', default=None))
                customer1 = Customer.objects.get(person__exact=person1)
                print(customer1)
                print("====")
                orders = orders.filter(customer__exact=customer1)


        if request.POST.get('project', default=None) is None:
            pass
        else:
            if request.POST.get('project', default=None) != '0':
                print(request.POST.get('project', default=None))
                project1 = Project.objects.get(name__exact=request.POST.get('project', default=None))
                orders = orders.filter(project__exact=project1)
            pass
        if request.POST.get('executed', default=None) is None:
            pass

    #print(emps)
    return render(request, 'analyzes/orders.html', {'orders':orders, 'types':types,'customers':customers,'projects':projects})


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

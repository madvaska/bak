from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze
from persons.models import Customer,Person
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

# Create your views here.
def orders(request, page):
    if not request.user.is_authenticated:
        raise PermissionDenied
        print('неавторизованный')
        return render(request, 'analyzes/orders.html')

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
    orders = Paginator(orders,1)
    if page is None:
        page_num = 1
    else:
        page_num = page
    try:
        orders = orders.page(page_num)
    except EmptyPage:
        orders = orders.page(1)
    print(orders.paginator.num_pages)
    return render(request, 'analyzes/orders.html', {'orders':orders, 'types':types,'customers':customers,
    'projects':projects,'typeselected':typeselected,'customerselected':customerselected,'projectselected':projectselected})

def order_details(request,id):
    if id is None:
        id = 1
    try:
        elem = Order.objects.get(pk=id)
    except ObjectDoesNotExist:
        print("нет записи в таблице order id = "+id)
        return redirect(reverse('orders',kwargs={'page':2}))
        pass
        #raise
    if elem.executed:
        analyze = Analyze.objects.get(order=elem)
        print(analyze.pk)
    else:
        analyze=None
    return render(request, 'analyzes/order_details.html', {'elem':elem, 'analyze':analyze})

def analyzeType(request):
    analyzeTypes = AnalyzeType.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzetypes.html', {'analyzeTypes':analyzeTypes})

def projects(request):
    projects = Project.objects.all()
    #print(emps)
    return render(request, 'analyzes/projects.html', {'projects':projects})

def analyzes(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
        print('неавторизованный')
        return render(request, 'analyzes/analyzes.html')
    analyzes = Analyze.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzes.html', {'analyzes':analyzes})

def analyze_details(request,id):
    analyze = Analyze.objects.get(pk=id)
    print(analyze)
    return render(request, 'analyzes/analyze_details.html', {'analyze':analyze})




#    url(r'^at/$', views.analyzeType, name='Типы анализов'),
#    url(r'^at/add', AddAnalyzeType.as_view(), name='Добавить новый тип анализов'),
#    url(r'^pr/$', views.projects, name='Проекты'),
#    url(r'^pr/add', AddProject.as_view(), name='Добавить новый проект'),

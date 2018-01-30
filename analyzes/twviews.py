from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze
from persons.models import Customer,Person
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage


class AddOrder(CreateView):
    model = Order
    fields = ['dateTime','code','codeOfSample','type','customer','project','comment','executed']
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})

class AddAnalyzeType(CreateView):
    model = AnalyzeType
    fields = ['code','name']
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})

class AddProject(CreateView):
    model = Project
    fields = ['name']
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})

class AddAnalyze(CreateView):
    model = Analyze
    fields = ['dateTime','order','analyst','appointedBy','comment','verifyed']

    def get_context_data(self, **kwargs):
        context = super(AddAnalyze,self).get_context_data(**kwargs)
        #print (self.kwargs)
        #or elem in kwargs:
        #    print("elem = "+elem)
        order = self.kwargs['order']
        if order is None:
            pass
        else:
            self.initial['order']=Order.objects.get(code=order)
            print(Order.objects.get(code=order))
        #print('Попали внутрь t_context_data. order = '+order)
        print(context)
        self.initial["verifyed"]=False
        return context
    # Создается на основании заявки
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})


#    url(r'^at/$', views.analyzeType, name='Типы анализов'),
#    url(r'^at/add', AddAnalyzeType.as_view(), name='Добавить новый тип анализов'),
#    url(r'^pr/$', views.projects, name='Проекты'),
#    url(r'^pr/add', AddProject.as_view(), name='Добавить новый проект'),

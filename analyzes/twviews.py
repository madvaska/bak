from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze
from persons.models import Customer,Person, Analyst
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.contrib.auth.models import User

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
    exclude =['order']
    success_url = "/a/o"


    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            print('auth')
            analyst = Analyst.objects.get(person__user=user)
            self.initial['analyst']=analyst
        else:
            print('not auth')
        print(user)

        order = self.kwargs['order']
        if order is None:
            print('notfind order')
        else:
            print('find order = '+order)
            print(Order.objects.get(code=order))
            self.initial['order']=Order.objects.get(code=order)
        self.initial["verifyed"]=True

        return super(AddAnalyze,self).get(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        print("test1")
        user = request.user
        if user.is_authenticated:
            print('auth post')
        else:
            print('not auth post')
        print(user)
        #form.instance.order = self.initial['order']
        return(super(AddAnalyze,self).post(request,*args,**kwargs))
        pass

    def form_valid(self,form):
        print("test2")
        print(user)
        form.instance.order = self.initial['order']
        return super(AddAnalyze,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddAnalyze,self).get_context_data(**kwargs)
        context['order'] = self.initial['order']
        context['analyst'] = self.initial['analyst']

        #print(context['form']['order'].is_hidden)
        #print (self.kwargs)
        #or elem in kwargs:
        #    print("elem = "+elem)
        #order = self.kwargs['order']
        #if order is None:
        #    pass
        #else:
        #    self.initial['order']=Order.objects.get(code=order)
        #    print(Order.objects.get(code=order))
        #print('Попали внутрь t_context_data. order = '+order)
        #print(context)
        return context
    # Создается на основании заявки
    #print('emps')
    #return render(request, 'persons/persons.html', {'emps':emps})


#    url(r'^at/$', views.analyzeType, name='Типы анализов'),
#    url(r'^at/add', AddAnalyzeType.as_view(), name='Добавить новый тип анализов'),
#    url(r'^pr/$', views.projects, name='Проекты'),
#    url(r'^pr/add', AddProject.as_view(), name='Добавить новый проект'),

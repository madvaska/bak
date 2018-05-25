from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze, OrdersCode, SamplesCode,Sample
from persons.models import Customer,Person, Analyst
from django.views.generic.edit import CreateView, ListView, UpdateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
import datetime

class AddOrder(CreateView):
    model = Order
    fields = ['dateTime','code','codeOfSample','type','customer','project','comment']
    success_url="/a/o/"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            customer = Customer.objects.get(person__user=user)
            self.initial['customer'] = customer
        else:
            raise Exception('You are not auth.')
        now = datetime.datetime.now()
        if now.month <10:
            str1 = str(now.year)+"0"+str(now.month)
        else:
            str1 = str(now.year)+str(now.month)
        try:
            ocode = OrdersCode.objects.get(pk=1)
            code1 = ocode.code
            ocode.code = str(int(code1)+1)
            ocode.save()
        except Exception:
            ocode = OrdersCode.objects.create(pk=1,code=str1 + "0001")
        if ocode.code < str1 + "0001":
            ocode.code = str1 + "0001"
            ocode.save()
        self.initial['code'] =  ocode.code
        #try:
        #    scode = SamplesCode.objects.get(pk=1)
        #    code1 = scode.codeOfSample
        #    scode.codeOfSample=str(int(code1)+1)
        #    scode.save()
        #except Exception:
        #    scode = SamplesCode.objects.create(pk=1,codeOfSample=str1+"0001")
        #if scode.codeOfSample < str1 + "0001":
        #    scode.codeOfSample = str1 + + "0001"
        #    scode.save()
        #self.initial['codeOfSample'] =  scode.codeOfSample
        return super(AddOrder,self).get(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        print("test1")
        print(request.POST)
        print(self)
        user = request.user
        if user.is_authenticated:
            print('auth post')
        else:
            print('not auth post')
            raise Exception('You are not auth.')
        return(super(AddOrder,self).post(request,*args,**kwargs))

    def form_valid(self,form):
        return super(AddOrder,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddOrder,self).get_context_data(**kwargs)
        context['customer'] = self.initial['customer']
        now = datetime.datetime.now()
        try:
            ocode = OrdersCode.objects.get(pk=1)
        except Exception:
            str1 = now.month
            if now.month < 10:
                str1 = "0"+str(now.month)
            ocode = OrdersCode.objects.create(pk=1,code=""+str(now.year)+str1+"0001")
        #context['code'] =  ocode.code
        try:
            scode = SamplesCode.objects.get(pk=1)
        except Exception:
            scode = SamplesCode.objects.create(pk=1,codeOfSample=""+str(now.year)+str1+"0001")
        #context['codeOfSample'] =  scode.codeOfSample
        #print(context['form'].fields['code'].disabled)
        #context['form'].fields['code'].disabled = True
        #print(context['form'].fields['code'].disabled)

        return context


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
            raise Exception('You are not auth.')
            return super(AddAnalyze,self).get(request, *args, **kwargs)
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
        #form.instance.order = self.initial['order']
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


class AddSample(CreateView):
    model = Sample
    #    dateTime = models.DateField(default=datetime.datetime.now,verbose_name='Дата')
    #    customer    = models.ForeignKey(Customer, verbose_name='Заказчик')
    #    code = models.CharField(max_length=20,unique=True,verbose_name='Код образца')
    #    status = models.BooleanField(default=False, verbose_name = 'Образец получен лабораторией')
    #    comment = models.TextField( blank = True, verbose_name='Описание образца' )

    fields = ['dateTime','customer','code','comment']
    #exclude =['order']
    success_url = "/a/s"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                customer = Customer.objects.get(person__user=user)
                self.initial['customer']=customer
            except Exception as e:
                raise Exception('You are not customer.')
        else:
            raise Exception('You are not auth.')

        return super(AddSample,self).get(request, *args, **kwargs)

    def form_valid(self,form):
        print("test2")
        user = self.initial['customer']
        try:
            customer = Customer.objects.get(pk=user.pk)
            form.instance.customer = customer
        except Exception as e:
            raise Exception('You are not customer.')
        return super(AddSample,self).form_valid(form)

class ListAnalyzeTypes(ListView)
    model = AnalyzeType
    fields = ['code','name','analyst']

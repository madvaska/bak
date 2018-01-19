from django.shortcuts import render
from .models import Order, Project, AnalyzeType
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

from django.shortcuts import render
from persons.models import Person, Customer, Administrator, Analyst
from django.contrib.auth.models import User

# Create your views here.
def welcome(request):
    user = request.user

    is_admin = False
    is_customer = False
    is_analyst = False
    is_super_analyst = False

    if user.is_authenticated:
        try:
            customer = Customer.objects.get(person__user = user)
        except :
            is_customer = False
        else:
            is_customer = True

        try:
            analyst = Analyst.objects.get(person__user__pk = user.pk)
            if analyst.isHead :
                is_super_analyst = True
            else:
                is_super_analyst = False
        except:
            is_analyst = False
        else:
            is_analyst = True

        try:
            Administrator.objects.get(person__user__pk = user.pk)
        except:
            is_admin = False
        else:
            is_admin = True
        print('Пользователь опледлен')

    #print(emps)
    return render(request, 'welcome/welcome.html', {'user':user,
'is_admin':is_admin,'is_customer':is_customer,'is_analyst':is_analyst,
'is_super_analyst':is_super_analyst})

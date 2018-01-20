from django.shortcuts import render

# Create your views here.
def welcome(request):
    user = request.user
    #print(emps)
    return render(request, 'welcome/welcome.html', {'user':user})

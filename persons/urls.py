"""bak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from persons.views import AddPersons, AddCustomer, AddAnalyst, AddAdministrator
from django.views.generic import CreateView
#from django.contrib import admin


urlpatterns = [
    url(r'^$', views.persons, name='users'),
    url(r'^pers/add', AddPersons.as_view(), name='adduser'),
    url(r'^c/$', views.customers, name='customers'),
    url(r'^c/add', AddCustomer.as_view(), name='addcustomer'),
    url(r'^a/$', views.analysts, name='analysts'),
    url(r'^a/add', AddAnalyst.as_view(), name='addanalyst'),
    url(r'^x/$', views.administrators, name='administrators'),
    url(r'^x/add', AddAdministrator.as_view(), name='addadministrator'),
]

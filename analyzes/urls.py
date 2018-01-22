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
from persons.views import AddPersons
from django.views.generic import CreateView
#from django.contrib import admin
from analyzes.views import AddOrder
from analyzes.views import AddAnalyzeType
from analyzes.views import AddProject
from analyzes.views import AddAnalyze


urlpatterns = [
    #url(r'^$', views.persons, name='сотрудники'),
    url(r'^o/$', views.orders, name='сотрудники'),
    url(r'^o/add', AddOrder.as_view(), name='сотрудники'),
    url(r'^at/$', views.analyzeType, name='Типы анализов'),
    url(r'^at/add', AddAnalyzeType.as_view(), name='Добавить новый тип анализов'),
    url(r'^pr/$', views.projects, name='Проекты'),
    url(r'^pr/add', AddProject.as_view(), name='Добавить новый проект'),
    url(r'^a/$', views.analyzes, name='Анализы'),
    url(r'^a/add', AddAnalyze.as_view(), name='Добавить новый анализ'),
]

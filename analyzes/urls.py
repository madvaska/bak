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
from analyzes.twviews import AddAnalyze, AddProject, AddAnalyzeType, AddOrder
from analyzes.twviews import AddSample, ListAnalyzeTypes


urlpatterns = [
    #url(r'^$', views.persons, name='сотрудники'),
    url(r'^o/(?P<page>\d+)?$', views.orders, name='orders'),
    url(r'^o/view/(?P<id>\d+)?$', views.order_details, name='order'),
    url(r'^o/add', AddOrder.as_view(), name='add_order'),
    url(r'^at/$', views.analyzeTypes, name='analyzetypes'),
    url(r'^at/add', AddAnalyzeType.as_view(), name='Добавить новый тип анализов'),
    url(r'^pr/$', views.projects, name='Проекты'),
    url(r'^pr/add', AddProject.as_view(), name='Добавить новый проект'),
    url(r'^a/$', views.analyzes, name='Анализы'),
    url(r'^a/view/(?P<id>\d+)?$', views.analyze_details, name='analyze'),
    url(r'^a/add/(?P<order>\d+)?$', AddAnalyze.as_view(), name='add_analyze'),
    url(r'^df/$', views.data_formats, name='dformats'),
    url(r'^df/edit/(?P<df>\d+)?$', views.data_format_edit, name='dformatedit'),
    url(r'^res/(?P<analyze_id>\d+)/(?P<df>\d+)$', views.show_res_for_analyze, name='viewres'),
    url(r'^s/(?P<page>\d+)?$', views.sample_details, name='samples'),
    url(r'^s/at/(?P<samplepk>\d+)?$', views.list_types, name='list_types'),
    url(r'^s/add', AddSample.as_view(), name='add_sample'),
    url(r'^report/', views.report, name='reports'),
    url(r'^atlist', ListAnalyzeTypes.as_view(), name='list_at'),
    #url(r'^soa/(?P<samplepk>\d+)?$', views.list_types, name='list_types'),
]

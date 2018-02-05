from django.contrib import admin
from .models import Order,Project,AnalyzeType,Analyze,AnalyzeDataFormat,DataFormatField
from .models import dataIntValue,DataTextValue,DataImageValue,DataXLSValue,DataBinaryValue
from .models import OrdersCode, SamplesCode
# Register your models here.
admin.site.register(Order)
admin.site.register(Project)
admin.site.register(AnalyzeType)
admin.site.register(Analyze)
admin.site.register(AnalyzeDataFormat)
admin.site.register(DataFormatField)
admin.site.register(dataIntValue)
admin.site.register(DataTextValue)
admin.site.register(DataImageValue)
admin.site.register(DataXLSValue)
admin.site.register(DataBinaryValue)
admin.site.register(OrdersCode)
admin.site.register(SamplesCode)

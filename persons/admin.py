from django.contrib import admin
from .models import Person,Department,PositionsAtWork,Customer,Analyst,Administrator
# Register your models here.
admin.site.register(Person)
admin.site.register(Department)
admin.site.register(PositionsAtWork)
admin.site.register(Customer)
admin.site.register(Analyst)
admin.site.register(Administrator)

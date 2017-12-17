from django.db import models

# Create your models here.

class Department(models.Model):
    # TODO: Define fields here
    name        = models.CharField(blank=True, max_length=100)
    parent      = models.ForeignKey(Department, blank=True, null = True)


    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __unicode__(self):
        pass

class PositionsAtWork(models.Model):
    # TODO: Define fields here
    name            = models.CharField(blank=True, max_length=100)
    atDepartment    = models.ForeignKey(Department)
    head = models.ForeignKey(PositionsAtWork,null=True,blank=True)

    class Meta:
        verbose_name = 'PositionsAtWork'
        verbose_name_plural = 'PositionsAtWorks'

    def __unicode__(self):
        pass

class Person(models.Model):
    firstName       = models.CharField(blank=True, max_length=100)
    middleName      = models.CharField(blank=True, max_length=100)
    lastName        = models.CharField(blank=True, max_length=100)
    department      = models.ForeignKey(Department)
    positionAtWork  = models.ForeignKey(PositionsAtWork)
    workSince       = models.DateField()
    dismissed       = models.DateField(null=True,blank=True)
    #подумать в какой таблице безопасней...
    #password        = models.CharField(blank=True, max_length=100)
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

class Customer(models.Model):
    # TODO: Define fields here
    addBy = models.ForeignKey(Person)


    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __unicode__(self):
        pass

class Analyst(models.Model):
    # TODO: Define fields here
    addBy = models.ForeignKey(Person)

    class Meta:
        verbose_name = 'Analyst'
        verbose_name_plural = 'Analysts'

    def __unicode__(self):
        pass

class Administrator(models.Model):
    # TODO: Define fields here
    addBy = models.ForeignKey(Person)

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'

    def __unicode__(self):
        pass

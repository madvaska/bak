from django.db import models

# Create your models here.

class Department(models.Model):
    # TODO: Define fields here
    name        = models.CharField(blank=True, max_length=100)
    parent      = models.ForeignKey('self', blank=True, null = True)


    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
        #pass

class PositionsAtWork(models.Model):
    # TODO: Define fields here
    name            = models.CharField(blank=True, max_length=100)
    atDepartment    = models.ForeignKey(Department)
    head = models.ForeignKey('self',null=True,blank=True)

    class Meta:
        verbose_name = 'PositionsAtWork'
        verbose_name_plural = 'PositionsAtWorks'

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

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

    def __unicode__(self):
        return self.lastName
    def __str__(self):
        return self.lastName

class Customer(models.Model):
    # TODO: Define fields here
    person = models.ForeignKey(Person)
    addBy = models.ForeignKey(Person,related_name="customer_addby",blank=True,default=None)
    def __unicode__(self):
        return self.person
    def __str__(self):
        return self.person.lastName

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __unicode__(self):
        pass

class Analyst(models.Model):
    # TODO: Define fields here
    person = models.ForeignKey(Person)
    addBy = models.ForeignKey(Person,related_name="analyst_addby",blank=True,default=None)
    #флаг что это руководитель
    isHead = models.BooleanField(default=False)
    def __unicode__(self):
        return self.person
    def __str__(self):
        return self.person.lastName

    class Meta:
        verbose_name = 'Analyst'
        verbose_name_plural = 'Analysts'

    def __unicode__(self):
        pass

class Administrator(models.Model):
    # TODO: Define fields here
    person = models.ForeignKey(Person)
    addBy = models.ForeignKey(Person,related_name="administrator_addby",blank=True,default=None)
    def __unicode__(self):
        return self.person
    def __str__(self):
        return self.person.lastName

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'

    def __unicode__(self):
        pass

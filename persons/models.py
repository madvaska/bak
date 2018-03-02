from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
    # TODO: Define fields here
    name        = models.CharField(blank=True, max_length=100, verbose_name='Название подразделения',unique=True)
    parent      = models.ForeignKey('self', blank=True, null = True, verbose_name='Родитель')


    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
        #pass

class PositionsAtWork(models.Model):
    # TODO: Define fields here
    name            = models.CharField(max_length=100, verbose_name='Должность')
    atDepartment    = models.ForeignKey(Department, verbose_name='Подразделение')
    head = models.ForeignKey('self',null=True,blank=True, verbose_name='Руководитель')

    class Meta:
        verbose_name = 'Занимаемая должность'
        verbose_name_plural = 'Занимаемые должности'

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Person(models.Model):
    #firstName       = models.CharField(blank=True, max_length=100)
    #middleName      = models.CharField(blank=True, max_length=100)
    #lastName        = models.CharField(blank=True, max_length=100)
    department      = models.ForeignKey(Department, verbose_name='Подразделения')
    positionAtWork  = models.ForeignKey(PositionsAtWork, verbose_name='Должность')
    workSince       = models.DateField(verbose_name='Работает с ')
    dismissed       = models.DateField(null=True,blank=True, verbose_name='Уволен с ')
    user            = models.OneToOneField(User, verbose_name='Пользователь')
    #подумать в какой таблице безопасней...
    #password        = models.CharField(blank=True, max_length=100)
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.user.username

class Customer(models.Model):
    # TODO: Define fields here
    person = models.OneToOneField(Person, verbose_name='Заказчик')
    addBy = models.ForeignKey(Person,related_name="customer_addby",blank=True,
    default=None, verbose_name='Добавлен пользователем')
    def __unicode__(self):
        return self.person
    def __str__(self):
        return self.person.user.username

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __unicode__(self):
        pass
    def __str__(self):
        return self.person.user.username

class Analyst(models.Model):
    # TODO: Define fields here
    person = models.OneToOneField(Person, verbose_name='Измеритель')
    addBy = models.ForeignKey(Person,related_name="analyst_addby",blank=True,
    default=None, verbose_name='Добавлен пользователем')
    #флаг что это руководитель
    isHead = models.BooleanField(default=False)
    def __unicode__(self):
        return self.person
    def __str__(self):
        return self.person.user.username

    class Meta:
        verbose_name = 'Измеритель'
        verbose_name_plural = 'Измерители'

    def __unicode__(self):
        pass
    def __str__(self):
        return self.person.user.username

class Administrator(models.Model):
    # TODO: Define fields here
    person = models.OneToOneField(Person, verbose_name='Администратор')
    addBy = models.ForeignKey(Person,related_name="administrator_addby",
    blank=True,default=None, verbose_name='Добавлен пользователем ')
    def __unicode__(self):
        return self.person
    def __str__(self):
        return self.person.lastName

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __unicode__(self):
        pass
    def __str__(self):
        return self.person.user.username

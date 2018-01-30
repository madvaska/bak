from django.db import models
from persons.models import Customer,Analyst
import datetime

# Create your models here.

class Project(models.Model):
    # TODO: Define fields here
    name = models.CharField(blank=True, max_length=100)
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.name)

class AnalyzeType(models.Model):
    # TODO: Define fields here
    code = models.CharField(unique=True,max_length=10, verbose_name='Код')
    name = models.CharField(unique=True,max_length=400, verbose_name='Наименование')
    class Meta:
        verbose_name = 'AnalyzeType'
        verbose_name_plural = 'AnalyzeTypes'

    def __unicode__(self):
        return(self.name)
        pass
    def __str__(self):
        return(self.code+"  "+self.name)
        pass

class Order(models.Model):
    # TODO: Define fields here
    dateTime    = models.DateTimeField(blank=True, default=datetime.datetime.now)
    code        = models.CharField(blank=True, max_length=100)
    codeOfSample= models.CharField(blank=True, max_length=100)
    type        = models.ForeignKey(AnalyzeType)
    customer    = models.ForeignKey(Customer)
    project     = models.ForeignKey(Project)
    comment     = models.TextField()
    #флаг что по этому заказу сделан анализ и данные введены
    executed    = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.code)

class Analyze(models.Model):
    # TODO: Define fields here
    dateTime    = models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата')
    order       = models.ForeignKey(Order, verbose_name='Заявка')
    analyst     = models.ForeignKey(Analyst,related_name='analyst', verbose_name='Исполнитель')
    appointedBy = models.ForeignKey(Analyst,related_name='appointedBy', verbose_name='Назначен')
    comment     = models.TextField(verbose_name='Комментарий')
    #этот флаг означает что измеритель ввел данные и проверил значение
    verifyed    = models.BooleanField(default=False, verbose_name='Данные введены ии проверены')

    class Meta:
        verbose_name = 'Analyze'
        verbose_name_plural = 'Analyzes'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.order.code)


class AnalyzeDataFormat(models.Model):
    # TODO: Define fields here
    type = models.ForeignKey(AnalyzeType)
    name = models.CharField(blank=True, max_length=100)
    #флаг подтверждающий актуальность формата
    enable = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'AnalyzeDataFormat'
        verbose_name_plural = 'AnalyzeDataFormats'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.name)

class DataFormatField(models.Model):
    # TODO: Define fields here
    listTypes = (
    ('int', 'int'),
    ('int', 'int'),
    ('int', 'int'),
    ('int', 'int'),
    )
    fieldName       = models.CharField(blank=True, max_length=100)
    fieldType       = models.CharField(blank=True, max_length=100, choices = listTypes, default=int)
    serialNumber    = models.IntegerField()
    optional        = models.BooleanField()

    #дальнейшие поля для отображения на форме ввода и для отражения в виде таблицы результатов
    fieldCaption    = models.CharField(blank=True, max_length=100)
    fieldWidth      = models.IntegerField()
    fieldWidthInTable      = models.IntegerField()

    class Meta:
        verbose_name = 'DataFormatField'
        verbose_name_plural = 'DataFormatFields'

    def __unicode__(self):
        pass

class DataValue(models.Model):
    # TODO: Define fields here
    analyze = models.ForeignKey(Analyze)
    dataFormatField = models.ForeignKey(DataFormatField)
    dateTime = models.DateTimeField(blank=True, default=datetime.datetime.now)

    class Meta:
        abstract = True

class dataIntValue(DataValue):
    # TODO: Define fields here
    value   = models.DecimalField(max_digits=10,decimal_places=3)

    class Meta:
        verbose_name = 'dataIntValue'
        verbose_name_plural = 'dataIntValues'

    def __unicode__(self):
        pass


class DataTextValue(DataValue):
    # TODO: Define fields here
    value   = models.TextField()

    class Meta:
        verbose_name = 'dataTextValue'
        verbose_name_plural = 'dataTextValues'

    def __unicode__(self):
        pass

class DataImageValue(DataValue):
    # TODO: Define fields here
    value   = models.ImageField()

    class Meta:
        verbose_name = 'dataImageValue'
        verbose_name_plural = 'dataImageValues'

    def __unicode__(self):
        pass

class DataXLSValue(DataValue):
    # TODO: Define fields here
    value   = models.FileField(upload_to='')

    class Meta:
        verbose_name = 'dataXLSValue'
        verbose_name_plural = 'dataXLSValues'

    def __unicode__(self):
        pass

class DataBinaryValue(DataValue):
    # TODO: Define fields here
    value   = models.BinaryField()

    class Meta:
        verbose_name = 'dataBinaryValue'
        verbose_name_plural = 'dataBinaryValues'

    def __unicode__(self):
        pass

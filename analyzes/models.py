from django.db import models
from persons.models import Customer,Analyst, Person, Administrator
import datetime

# Create your models here.

class Project(models.Model):
    # TODO: Define fields here
    name = models.CharField(blank=True, max_length=100,unique=True)
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

class OrdersCode(models.Model):
    code        = models.CharField(max_length=20,unique=True,verbose_name='Код заявки')

    def __str__(self):
        return(self.code)

    def __unicode__(self):
        return u"orders_code"

class SamplesCode(models.Model):
    codeOfSample= models.CharField(max_length=20,unique=True,verbose_name='Код образца')

    def __str__(self):
        return(self.codeOfSample)

    def __unicode__(self):
        return u"orders_code"


class Order(models.Model):
    # TODO: Define fields here
    dateTime    = models.DateTimeField(default=datetime.datetime.now,verbose_name='Дата')
    code        = models.CharField(max_length=20,unique=True,verbose_name='Код заявки')
    codeOfSample= models.CharField(max_length=20,unique=True,verbose_name='Код образца')
    type        = models.ForeignKey(AnalyzeType, verbose_name='Тип анализа')
    customer    = models.ForeignKey(Customer, verbose_name='Заказчик')
    project     = models.ForeignKey(Project, verbose_name='Проект')
    comment     = models.TextField(blank=True, verbose_name='Комментарий')
    #флаг что по этому заказу сделан анализ и данные введены
    executed    = models.BooleanField(default=False, verbose_name='Анализ сделан и данные введены')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.code)

class SetAnalyst(models.Model):
    order = models.ForeignKey(Order, unique=True)
    Analyst = models.ForeignKey(Analyst)
    assignBy = models.ForeignKey(Person)
    class Meta:
        verbose_name = 'Назначение измерителя'
        verbose_name_plural = 'Назначения измерителя'
    def __unicode__(self):
        return uSetAnalyst
    def __str__(self):
        return(self.order.code)

class DeliverySample(models.Model):
    order = models.ForeignKey(Order, unique = True)
    success = models.BooleanField(default = False)
    class Meta:
        verbose_name = 'Доставка образца'
        verbose_name_plural = 'Доставки образцов'
    def __unicode__(self):
        return uDeliverySample
    def __str__(self):
        return(self.order.codeOfSample)

class Analyze(models.Model):
    # TODO: Define fields here
    dateTime    = models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата')
    order       = models.ForeignKey(Order, verbose_name='Заявка',unique=True)
    analyst     = models.ForeignKey(Analyst,related_name='analyst', verbose_name='Исполнитель')
    appointedBy = models.ForeignKey(Analyst,related_name='appointedBy', verbose_name='Назначен')
    comment     = models.TextField(blank=True,verbose_name='Комментарий')
    #этот флаг означает что измеритель ввел данные и проверил значение
    verifyed    = models.BooleanField(default=False, verbose_name='Данные введены ии проверены')

    class Meta:
        verbose_name = 'Анализ'
        verbose_name_plural = 'Анализы'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.order.code)


class AnalyzeDataFormat(models.Model):
    # TODO: Define fields here
    type = models.ForeignKey(AnalyzeType,verbose_name='Тип анализа')
    name = models.CharField(blank=True, max_length=100, unique=True,verbose_name='Наименование формата')
    #флаг подтверждающий актуальность формата
    enable = models.BooleanField(default=True,verbose_name='Активен')

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
    ('int', 'Число'),
    ('text', 'Текст'),
    ('img', 'Картинка'),
    ('xls', 'Файл XLS'),
    ('bin', 'Двоичный файл'),
    )
    dataFormat = models.ForeignKey(AnalyzeDataFormat,verbose_name='Формат данных')
    fieldName       = models.CharField(blank=True, max_length=100,verbose_name='Имя поля')
    fieldType       = models.CharField(blank=True, max_length=100, choices = listTypes,
    default=int,verbose_name='Тип данных в поле')
    serialNumber    = models.IntegerField(verbose_name='Код поля')
    optional        = models.BooleanField(verbose_name='Обязательность заполнения')

    #дальнейшие поля для отображения на форме ввода и для отражения в виде таблицы результатов
    fieldCaption    = models.CharField(blank=True, max_length=100,verbose_name='Заголовок поля')
    fieldWidth      = models.IntegerField(verbose_name='Ширина поля')
    fieldWidthInTable      = models.IntegerField(verbose_name='Ширина поля в таблице')

    class Meta:
        verbose_name = 'DataFormatField'
        verbose_name_plural = 'DataFormatFields'

    def __unicode__(self):
        pass
    def __str__(self):
        return(self.fieldType)

class DataValue(models.Model):
    # TODO: Define fields here
    analyze = models.ForeignKey(Analyze,verbose_name='Анализ')
    dataFormatField = models.ForeignKey(DataFormatField,verbose_name='Шаблон ввода данных')
    dateTime = models.DateTimeField(blank=True, default=datetime.datetime.now,verbose_name='Дата ввода')

    class Meta:
        abstract = True

class dataIntValue(DataValue):
    # TODO: Define fields here
    value   = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Значение')

    class Meta:
        verbose_name = 'dataIntValue'
        verbose_name_plural = 'dataIntValues'

    def __unicode__(self):
        pass

class DataTextValue(DataValue):
    # TODO: Define fields here
    value   = models.TextField(verbose_name='Значение')

    class Meta:
        verbose_name = 'dataTextValue'
        verbose_name_plural = 'dataTextValues'

    def __unicode__(self):
        pass

class DataImageValue(DataValue):
    # TODO: Define fields here
    value   = models.ImageField(verbose_name='Значение')

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

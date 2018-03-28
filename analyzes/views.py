from django.shortcuts import render
from .models import Order, Project, AnalyzeType, Analyze
from .models import AnalyzeDataFormat, DataFormatField
from .models import SetAnalyst
from .models import OrdersCode
from .models import Sample
from persons.models import Customer,Person,Analyst,Administrator
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
import datetime


def getNewCodeOrder():
    now = datetime.datetime.now()
    if now.month <10:
        str1 = str(now.year)+"0"+str(now.month)
    else:
        str1 = str(now.year)+str(now.month)
    try:
        ocode = OrdersCode.objects.get(pk=1)
        code1 = ocode.code
        ocode.code = str(int(code1)+1)
        ocode.save()
    except Exception:
        ocode = OrdersCode.objects.create(pk=1,code=str1 + "0001")
    if ocode.code < str1 + "0001":
        ocode.code = str1 + "0001"
        ocode.save()

    return(ocode.code)

def getUserRole(request):
    auth = False
    customer = None
    superAnalyst = None
    analyst = None
    admin = None
    user = request.user
    if user.is_authenticated:
        auth = True
        try:
            customer = Customer.objects.get(person__user = user)
        except Exception as e:
            pass
        try:
            analyst = Analyst.objects.get(person__user = user)
            if analyst.isHead:
                superAnalyst = analyst
        except Exception as e:
            pass
        try:
            admin = Administrator.objects.get(person__user = user)
        except Exception as e:
            pass
        return({'user':user,'auth':auth,'customer':customer,'analyst':analyst,'superAnalyst':superAnalyst,'admin':admin})

def getSampleStatus(sample):
    status = 0
    #Статусы
    #   0   -   просто образец
    #   1   -   сделаны заказы испытаний
    #   2   -   назначены испытатели
    #   3   -   получен образец
    #   4   -   испытания частично завершены
    #   5   -   все испытания завершены
    try:
        orders = sample.ordersam.all()
        if len(orders) == 0:
            raise
        status = 1
        pass
    except Exception as e:
        pass
    else:
        try:
            for order in orders:
                setAnalyst = order.analyst
                print(setAnalyst)
        except Exception as e:
            pass
        else:
            status = 2
            if sample.status:
                status=3
                accFlag = True
                for order in orders:
                    if order.executed:
                        status = 4
                    else:
                        accFlag = False
                if status and accFlag:
                    status = 5
    return status


def getOrderStatus(order):
    return None

def orders(request, page):
    if not request.user.is_authenticated:
        raise PermissionDenied
        print('неавторизованный')
        return render(request, 'analyzes/orders.html')

    user = request.user
    print(user)
    #TODO
    #здесь нужно добавить проверку прав пользователя
    #
    #


    rules={'is_customer':False, 'is_analyst':False,
    'is_super_analyst':False, 'is_admin':False}


    try:
        customer = Customer.objects.get(person__user = user)
        rules['is_customer'] = True
    except :
        pass

    try:
        analyst = Analyst.objects.get(person__user__pk = user.pk)
        rules['is_analyst'] = True
        if analyst.isHead :
            rules['is_super_analyst'] = True
    except:
        pass

    try:
        admin = Administrator.objects.get(person__user = user)
        rules['is_admin'] = True
    except :
        pass

    if (rules['is_customer'] or rules['is_analyst'] or rules['is_super_analyst'] or rules['is_admin']):
        pass
    else:
        #TODO Нужно послать на хуй
        raise Exception('Пошел на фиг.')
        return render(request, 'analyzes/orders.html' )

    types = AnalyzeType.objects.all().order_by('code')
    projects = Project.objects.all().order_by('name')
    print('trace1')
    if (rules['is_admin'] or rules['is_super_analyst']):
        print('trace2.1')
        customers = Customer.objects.all().order_by('person__user__last_name')
    elif (rules['is_customer']):
        print('trace2.2')
        customers = Customer.objects.filter(person__user = user).order_by('person__user__last_name')
    else:
        print('trace2.3')
        customers = Customer.objects.filter(person__user = user).order_by('person__user__last_name')

    typeselected = ""
    customerselected = ''
    projectselected = ''

    if request.POST.get('but1', default=None) is None:
        if (rules['is_admin'] or rules['is_super_analyst']):
            orders = Order.objects.all().order_by('-dateTime')
        elif (rules['is_customer']):
            orders = Order.objects.filter(customer__person__user = user).order_by('-dateTime')
    else:
        str1 = ''
        if (rules['is_admin'] or rules['is_super_analyst']):
            orders = Order.objects.all().order_by('-dateTime')
        elif (rules['is_customer']):
            orders = Order.objects.filter(customer__person__user = user).order_by('-dateTime')

        typeselected = request.POST.get('type', default=None)
        if typeselected is None:
            pass
        else:
            typeselected = int(typeselected)
            if typeselected != 0:
                print('typeselected')
                print(typeselected)
                orders = orders.filter(type__pk=typeselected)
        customerselected = request.POST.get('customer', default=None)
        if customerselected is None:
            pass
        else:
            customerselected = int(customerselected)
            if customerselected != 0:
                orders = orders.filter(customer__pk=customerselected)

        projectselected = request.POST.get('project', default=None)
        if projectselected is None:
            pass
        else:
            projectselected = int(projectselected)
            if projectselected != 0:
                orders = orders.filter(project__pk=projectselected)
            pass
        if request.POST.get('executed', default=None) is None:
            pass

    if typeselected is None:
        typeselected = ''
    if customerselected is None:
        customerselected = ''
    if projectselected is None:
        projectselected = ''
    #print("dd="+customerselected)
    orders = Paginator(orders,30)
    if page is None:
        page_num = 1
    else:
        page_num = page
    try:
        orders = orders.page(page_num)
    except EmptyPage:
        orders = orders.page(1)
    for elem in orders:
        try:
            analyze = Analyze.objects.get(order=elem)
            if elem.executed:
                pass
            else:
                elem.executed = True
                elem.save()
        except :
            analyze=None
            if elem.executed:
                elem.executed = False
                elem.save()


    print(orders.paginator.num_pages)
    return render(request, 'analyzes/orders.html', {'orders':orders, 'types':types,'customers':customers,
    'projects':projects,'typeselected':typeselected,'customerselected':customerselected,'projectselected':projectselected})

def order_details(request,id):
    if id is None:
        id = 1
    try:
        elem = Order.objects.get(pk=id)
    except ObjectDoesNotExist:
        print("нет записи в таблице order id = "+id)
        return redirect(reverse('orders',kwargs={'page':2}))
        pass
        #raise

    try:
        analyze = Analyze.objects.get(order=elem)
        if elem.executed:
            pass
        else:
            elem.executed = True
            elem.save()
    except :
        analyze=None
        if elem.executed:
            elem.executed = False
            elem.save()
        else:
            pass
    else:
        pass
    return render(request, 'analyzes/order_details.html', {'elem':elem, 'analyze':analyze})

def analyzeTypes(request):
    types = AnalyzeType.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzetypes.html', {'analyzetypes':types})

def projects(request):
    projects = Project.objects.all()
    #print(emps)
    return render(request, 'analyzes/projects.html', {'projects':projects})

def analyzes(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
        print('неавторизованный')
        return render(request, 'analyzes/analyzes.html')
    analyzes = Analyze.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzes.html', {'analyzes':analyzes})

def analyze_details(request,id):
    analyze = Analyze.objects.get(pk=id)
    print(analyze)
    return render(request, 'analyzes/analyze_details.html', {'analyze':analyze})

#===============================================================================
#
#
#===============================================================================
def data_formats(request):
    try:
        atype = request.POST['atype']
        print(atype)
        #dformats = DataFormat.objects.all().filter(atype__pk=atype)
        dformats = AnalyzeDataFormat.objects.all().filter(type__pk=atype)
        print(dformats)
        atype = AnalyzeType.objects.get(pk=atype)
        at = atype.code
    except Exception:
        atype ="0"
        at = 'NOR'
        dformats = None
    #print(atype)

    atypes = AnalyzeType.objects.all().order_by('code')
    return render(request, 'analyzes/data_formats.html', {'dformats':dformats,'atypes':atypes, 'at':at})

#===============================================================================
#
#
#===============================================================================
def data_format_edit(request, df):
    if df is None:
        pass
    dataFormat = AnalyzeDataFormat.objects.get(pk=df)
    dataFormatFields = DataFormatField.objects.filter(dataFormat__pk=df)
    print(dataFormatFields[0])
    return render(request, 'analyzes/data_format_edit.html', {'dffs':dataFormatFields,'df':dataFormat})

#===============================================================================
#
#
#===============================================================================
def  show_res_for_analyze(request, analyze_id, df):
    #проверка можно ли пользоватедю смотреть результаты этого анализа

    #проверяем есть ли формат для анализа,  если есть, то есть ли результаты
    analyze = Analyze.objects.get(pk=analyze_id)
    id_atype = analyze.order.type.pk
    dataFormats = AnalyzeDataFormat.objects.filter(type__pk=id_atype)
    dfcount = dataFormats.count()
    if dfcount < 1 :
        #нет формата для этого типа анализов. сформировать ошибку. Показать пользователю
        pass
    else:
        if (dfcount == 1):
            #формат в точности один. Проверяем активность. Если активен показываем
            df = dataFormats[0]
            if df.enable == False:

                #ошибка нет активных форматов. Показать ошибку
                pass
        else:
            counter_enable = 0
            for df1 in dataFormats:
                if df1.enable:
                    counter_enable = counter_enable + 1
                    df = df1
            if counter_enable != 1 :
                #Ошибка либо нет активных форматов либо их слишком много. Показываем
                pass
    # у нас есть анализ и формат данных. Получаем для этого формата данных поля формата данных
    # если полей формата нет, то это ошибка сообщаем пользователю об этом
    dffs = DataFormatField.objects.filter(dataFormat=df)
    dffs_counter = dffs.count()
    if dffs_counter < 1:
        #Ошибка нет описания формата полей. Необходимо сначала настроить поля формата
        #Сообщаем об этом пользователю
        pass
    #    listTypes = (
    #    ('int', 'Число'),
    #    ('text', 'Текст'),
    #    ('img', 'Картинка'),
    #    ('xls', 'Файл XLS'),
    #    ('bin', 'Двоичный файл'),
    #    )
    res = []
    for dff in dffs:
        if dff.fieldType == 'int':
            res.append(dataIntValue.objects.filter(DataFormatField=dff).first())
        elif dff.fieldType == 'text':
            res.append(DataTextValue.objects.filter(DataFormatField=dff).first())
        elif dff.fieldType == 'img':
            res.append(DataImageValue.objects.filter(DataFormatField=dff).first())
        elif dff.fieldType == 'xls':
            res.append(DataTextXValue.objects.filter(DataFormatField=dff).first())
        elif dff.fieldType == 'bin':
            res.append(DataBinaryValue.objects.filter(DataFormatField=dff).first())
        else:
            #Тут какая то ошибка по видимому....
            pass

    #если да, то регистрируем этот запрос (что пришел пользователь
    #и ему показали результат, если он есть)


    #если форматы есть а результатов нет, то проверяем имеет ли пользователь
    #право внести результаты
    if len(res) == 0:
        #нужно вводить результаты (обязательность полей проверяем при вводе!)
        #проверяем может ли пользователь вводить результаты
        #точнее совпвдвет ли пользователь с пользователем в поле analyst analyze
        #выводим форму для ввода
        #нужно вводить недостающие (хотя может лучше обыграть обязательность поля....)
        pass
    else:
        # достаточно просто показать результаты
        pass

    #
    #
    #
    #
    #
    #
    #
    #
#===============================================================================
#
#
#===============================================================================
def sample_details(request, page):
    role = getUserRole(request)
    print(request.POST)
    if role['superAnalyst']:
        samples = Sample.objects.all().prefetch_related('ordersam').order_by("dateTime")
        samplepk = request.POST.get('samplepk',default=None)
        analystpk = request.POST.get('analystpk',default=None)
        print("samplepk")
        print(samplepk)
        if samplepk is None:
            pass
        else:
            try:
                analyst = Analyst.objects.get(pk=int(analystpk))
            except Exception as e:
                pass
            else:
                sample = Sample.objects.prefetch_related('ordersam').get(pk=int(samplepk))
                orders = sample.ordersam.all()
                print("orders")
                print(orders)
                for order in orders:
                    try:
                        setAnalyst=order.analyst
                        print(setAnalyst)
                        pass
                    except Exception as e:
                        print("нет")
                        SetAnalyst.objects.create(order=order,analyst=analyst,assignBy=role['analyst'].person)

    #Аналитик
    elif role['analyst']:
        samples = []
        orders = Order.objects.all().prefetch_related('analyst').filter(analyst__analyst=role['analyst']).order_by("dateTime")
        for order in orders:
            if samples.count(order.codeOfSample) == 0:
                samples.append(order.codeOfSample)
    #Заказчик
    elif role['customer']:
        samples = Sample.objects.filter(customer=role['customer']).prefetch_related('ordersam').order_by("dateTime")
    else:
        samples = []
        pass


    samples = Paginator(samples,6)
    if page is None:
        page_num = 1
    else:
        page_num = page
    try:
        samples = samples.page(page_num)
    except EmptyPage:
        samples = samples.page(1)

    for sample in samples:
        atype=[]
        orders = sample.ordersam.all()
        for order in orders:
            atype.append(order.type.code)
        sample.atype = orders
        sample.fullStatus = getSampleStatus(sample)
    atypes = AnalyzeType.objects.all()
    customers = Customer.objects.all()

    return render(request, 'analyzes/samples.html', {'page':page,
    'samples':samples,'atypes':atypes,'role':role, 'customers':customers})


#===============================================================================
#
#
#===============================================================================
def list_types(request, samplepk):
    if samplepk is None:
        return
    # TODO: если пользователь не авторизован или пользователь не заказчик или не
    # не СуперАналитик
    # не Аналитик тогда нефиг его сюда пускать
    roles = getUserRole(request)

    # TODO: Если пользователь заказчик
    user = request.user
    sample = Sample.objects.get(pk=samplepk)
    #получаем все типы анализов
    atypes = AnalyzeType.objects.all()
    atype = request.POST.getlist('atype',default=None)
    projectpk = request.POST.get('project',default=None)
    if projectpk is None:
        project = None
    else:
        project =  Project.objects.get(pk=projectpk)
    print("project = "+str(project))
    projects = Project.objects.all()
    #print(atype)
    #получаем все заказы для этого образца
    orders = Order.objects.filter(codeOfSample=sample)
    yettypes = []
    for order in orders:
        yettypes.append(order.type.pk)
    for at in atype:
        value = int(at)
        if value in yettypes:
            print('Уже есть '+str(value))
            continue
        #dateTime    = models.DateTimeField(default=datetime.datetime.now,verbose_name='Дата')
        #code        = models.CharField(max_length=20,unique=True,verbose_name='Код заявки')
        #codeOfSample= models.ForeignKey(Sample, default = None, blank =True, verbose_name='Код образца')
        #type        = models.ForeignKey(AnalyzeType, verbose_name='Тип анализа')
        #customer    = models.ForeignKey(Customer, verbose_name='Заказчик')
        #project     = models.ForeignKey(Project, verbose_name='Проект')
        #comment     = models.TextField(blank=True, verbose_name='Комментарий')
        #флаг что по этому заказу сделан анализ и данные введены
        #executed    = models.BooleanField(default=False, verbose_name='Анализ сделан и данные введены')
        #создать новый заказ
        Order.objects.create(
        code = getNewCodeOrder(),
        codeOfSample=sample,
        type=AnalyzeType.objects.get(pk=value),
        customer=Customer.objects.get(person__user=user),
        project=project,
        executed=False
        )
    #добавить новый заказ к заказам
    orders = Order.objects.filter(codeOfSample=sample)
    return render(request, 'analyzes/lt.html', {'sample':sample,'atypes':atypes,'orders':orders,'projects':projects})

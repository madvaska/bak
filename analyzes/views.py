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
from django.core.mail import send_mail
import datetime
from django.utils import timezone
#test
from reportlab.pdfgen import canvas
from django.http import HttpResponse


#===============================================================================
#
#
#===============================================================================
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

#===============================================================================
#
#
#===============================================================================
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

#===============================================================================
#
#
#===============================================================================
def getSampleStatus(sample):
    status = 0
    #Статусы
    #   0   -   просто образец
    #   1   -   сделаны заказы испытаний
    #   2   -   назначены ВСЕ испытатели
    #   3   -   получен образец
    #   4   -   получен образец И назначены ВСЕ испытатели
    #   5   -   испытания частично завершены
    #   6   -   все испытания завершены
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
            if sample.status:
                status=3
            pass
        else:
            status = 2
            if sample.status:
                status=4
                accFlag = True
                for order in orders:
                    if order.executed:
                        status = 5
                    else:
                        accFlag = False
                if status and accFlag:
                    status = 6
    return status

#===============================================================================
#
#
#===============================================================================
def getOrderStatus(order):
    return None


#===============================================================================
#
#
#===============================================================================
def getFormName(POSTDICT, formlist):

    for key in POSTDICT:
        print("Key = %s"%key)
        for key2 in formlist:
            print("Key2 = %s"%key2)
            print(formlist[key2])
            if key in formlist[key2]:
                return (key2,key)
    return None


#===============================================================================
#
#
#===============================================================================
def orders(request, page):
    error = None
    role = getUserRole(request)
    analysts = Analyst.objects.all()
    if role['auth'] == False:
        error="Необходимо авторизоваться"
    elif (role['superAnalyst'] is not None) or (role['admin'] is not None):
        orders = Order.objects.all().order_by('-codeOfSample__dateTime')
        pass
    else: # либо аналитик либо заказчик, либо и то и другое
        if (role['customer'] is not None) and (role['analyst'] is not None):
            # TODO: order
            orders1 = Order.objects.filter(customer=role['customer']).order_by('-codeOfSample__dateTime')
            orders2 = Order.objects.exclude(analyst__isnull=False).filter(analyst__analyst=role['analyst']).order_by('-codeOfSample__dateTime')
        elif (role['customer'] is not None):
            orders = Order.objects.filter(customer=role['customer']).order_by('-codeOfSample__dateTime')
        elif (role['analyst'] is not None):
            orders = Order.objects.exclude(analyst__isnull=False).filter(analyst__analyst=role['analyst']).order_by('-codeOfSample__dateTime')
        else:
            error='Не предвиденный тип пользователя.'
        pass
    pass
    if error is not None:
        return render(request, 'analyzes/error.html', {'error':error})

    if len(request.POST) > 0 : #Обработаем форзвращенные значения формы
        typeselected = ""
        customerselected = ''
        projectselected = ''
        #0. Зададим список форм которые мы обрабатываем в этой функции
        formlist = {'newOrder':{'newOrder':'newOrder'},
        'filter':{'filterOn':'filterOn','filterOff':'filterOff'},
        'setAnalyst':{'setAnalyst':'setAnalyst'},
        'orderexecute':{'orderexecute':'orderexecute'},}
        #1. Определим данные какой формы пришли
        formName = getFormName(request.POST, formlist)
        #1.1 Если не смогли определить форму, то сохраним ошибку
        # и покажем её на странице
        if formName is None:
            error="Не определена форма. Свяжитесь с разработчиком."
        #1.2 Если смогли то продолжим обработку
        #2. Проверим имеет ли пользователь право работать с этой формой
        #2.1. Если нет, то формируем ошибку и покажем это на странице

        if formName[0] == 'newOrder':
            if role['customer'] is None:
                error="Новый заказ может сделать только заказчик"
        elif formName[0] == 'filter':
            if role['auth'] == False:
                error="Только авторизованный пользователь может просматривать заказы"
        elif formName[0] == 'setAnalyst':
            if role['superAnalyst'] is None:
                error="Только суперАналитик может назначать измерителей"
        elif formName[0] == 'orderexecute':
            if role['superAnalyst'] or role['analyst']:
                pass
            else:
                error = "Только измеритель или руководитель проставлять информацию об исполнени"
        else:
            error="Форма не опознана. Обратитесь к разработчику."
        #2.2. Если да, то продолжим
        #3. Определим что форма заполнена корректно
        #3.1. Проверим существуют ли объекты указанные в данных
        if formName[0] == 'newOrder':
            # TODO:
            pass
        elif formName[0] == 'filter':
            # TODO:
            try:
                selectedCustomer = None
                selectedType = None
                selectedProject = None
                customerpk = int(request.POST.get('customer',default=None))
                if (customerpk is not None) and (customerpk != 0):
                    selectedCustomer = Customer.objects.get(pk=customerpk)
                typepk = int(request.POST.get('type',default=None))
                if (typepk is not None) and (typepk != 0):
                    selectedType = AnalyzeType.objects.get(pk=typepk)
                projectpk = int(request.POST.get('project',default=None))
                if (projectpk is not None) and (projectpk != 0):
                    selectedProject = Project.objects.get(pk=projectpk)
            except Exception as e:
                error="Не найдены указанные объекты"
        elif formName[0] == 'setAnalyst':
            try:
                analyst = Analyst.objects.get(pk=request.POST.get('selectAnalystpk',default=None))
            except Exception as e:
                error="Введен несуществующий измеритель"
            try:
                order = Order.objects.get(pk=request.POST.get('orderpk',default=None))
            except Exception as e:
                error="Выбран несуществующий заказ"
            else:
                pass
            pass
        elif formName[0] == 'orderexecute':
            try:
                orderpk =int(request.POST.get('orderpk',default=None))
                if orderpk>0:
                    order = Order.objects.get(pk=orderpk)
            except Exception as e:
                error="Что то пошло не так"
        #3.2. Проверим имеет ли пользователь право выполнять требуемые  операции
        # с указанными объектами
        # TODO:
        if formName[0] == 'newOrder':
            # TODO:
            pass
        elif formName[0] == 'filter':
            # TODO:
            pass
        elif formName[0] == 'setAnalyst':
            try:
                temp = order.analyst
                error="Уже назначен измеритель для заказа"
            except Exception as e:
                pass
            if order.executed:
                error="Заказ уже выполнен"
            pass
        elif formName[0] == 'orderexecute':
            if role['analyst'] and not error:
                try:
                    analyst = order.analyst.analyst
                    if analyst != role['analyst']:
                        error = "Нельзя закрывать не свои заказы."
                except Exception as e:
                    error = "Не назначенного измерителя "+str(e)
        #3.3. Если некоректно то сохраним ошибку и покажем её на странице
        # TODO:
        #3.4. Если корректно то продолжим
        #4. Обработаем полученные данные
        # TODO:
        if formName[0] == 'newOrder':
            # TODO:
            pass
        elif formName[0] == 'filter':
            # TODO:
            if selectedCustomer is not None:
                orders = orders.filter(customer = selectedCustomer)
                customerselected = selectedCustomer.pk
            if selectedType is not None:
                orders = orders.filter(type = selectedType)
                typeselected = selectedType.pk
            if selectedProject is not None:
                orders = orders.filter(project = selectedProject)
                projectselected = selectedProject.pk
        elif formName[0] == 'setAnalyst':
            try:
                SetAnalyst.objects.create(order=order,analyst=analyst,assignBy=role['superAnalyst'].person)
                email = analyst.person.user.email
                if email is not None:
                    send_mail('Вам назначен заказ '+order.code, 'Номер образца '+str(order.codeOfSample)+', тип анализа: '+ str(order.type), 'admin@catalyst.su',
                    [email], fail_silently=False)
            except Exception as e:
                error = "Произошла ошибка. "+str(e)
            else:
                pass
            pass
        elif formName[0] == 'orderexecute':
            if not error:
                order.executed = True
                order.executedDateTime = timezone.now()
                order.save()


        #4.1 Если данные не удалось обработать, то сохраняем ошибку
        # и покажем её на странице
        if error is not None:
            print("error = %s"%error)
            return render(request, 'analyzes/error.html', {'error':error})
        #4.2 Если данные успешно обработаны, то продолжим отрисовку страницы

    else: #Нет данных посланных пост. необходимо начальное заполнение
        typeselected = ""
        customerselected = ''
        projectselected = ''
        if role['auth'] == False:
            error="Необходимо авторизоваться"
        elif (role['superAnalyst'] is not None) or (role['admin'] is not None):
            orders = Order.objects.all().order_by('-codeOfSample__dateTime')
            pass
        else: # либо аналитик либо заказчик, либо и то и другое
            if (role['customer'] is not None) and (role['analyst'] is not None):
                # TODO: order
                orders1 = Order.objects.filter(customer=role['customer']).order_by('-codeOfSample__dateTime')
                orders2 = Order.objects.exclude(analyst__isnull=False).filter(analyst__analyst=role['analyst']).order_by('-codeOfSample__dateTime')

            elif (role['customer'] is not None):
                orders = Order.objects.filter(customer=role['customer']).order_by('-codeOfSample__dateTime')
            elif (role['analyst'] is not None):
                orders = Order.objects.exclude(analyst__isnull=False).filter(analyst__analyst=role['analyst']).order_by('-codeOfSample__dateTime')
            else:
                error='Не предвиденный тип пользователя.'
            pass
        pass

    types = AnalyzeType.objects.all().order_by('code')
    projects = Project.objects.all().order_by('name')
    customers = Customer.objects.all().order_by('person__user__last_name')


    #print("dd="+customerselected)
    try:
        orders = Paginator(orders,30)
    except Exception as e:
        orders=[]
        orders = Paginator(orders,30)

    if page is None:
        page_num = 1
    else:
        page_num = page
    try:
        orders = orders.page(page_num)
    except EmptyPage:
        orders = orders.page(1)
    #for elem in orders:
    #    try:
    #        analyze = Analyze.objects.get(order=elem)
    #        if elem.executed:
    #            pass
    #        else:
    #            elem.executed = True
    #            elem.save()
    #    except :
    #        analyze=None
    #        if elem.executed:
    #            elem.executed = False
    #            elem.save()


    print(orders.paginator.num_pages)
    return render(request, 'analyzes/orders.html', {'orders':orders, 'types':types,'customers':customers,
    'projects':projects,'typeselected':typeselected,'customerselected':customerselected,'projectselected':projectselected,
    'analysts':analysts})

#===============================================================================
#
#
#===============================================================================
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

#===============================================================================
#
#
#===============================================================================
def analyzeTypes(request):
    types = AnalyzeType.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzetypes.html', {'analyzetypes':types})

#===============================================================================
#
#
#===============================================================================
def projects(request):
    projects = Project.objects.all()
    #print(emps)
    return render(request, 'analyzes/projects.html', {'projects':projects})

#===============================================================================
#
#
#===============================================================================
def analyzes(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
        print('неавторизованный')
        return render(request, 'analyzes/analyzes.html')
    analyzes = Analyze.objects.all()
    #print(emps)
    return render(request, 'analyzes/analyzes.html', {'analyzes':analyzes})

#===============================================================================
#
#
#===============================================================================
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
        samplepk = request.POST.get('samplepk',default=None)
        analystpk = request.POST.get('analystpk',default=None)
        setstatus = request.POST.get('setstatus',default=None)
        #print("samplepk")
        #print(samplepk)
        if setstatus:
            sample = Sample.objects.prefetch_related('ordersam').get(pk=int(samplepk))
            if getSampleStatus(sample) ==2:
                sample.status = True;
                sample.save()
            else:
                error = "Нельзя получать образец до добавления методов и назначения измерителей."
                return render(request, 'analyzes/error.html', {'error':error})
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
                for order in orders:
                    try:
                        setAnalyst=order.analyst
                        pass
                    except Exception as e:
                        SetAnalyst.objects.create(order=order,analyst=analyst,assignBy=role['analyst'].person)
        samples = Sample.objects.all().prefetch_related('ordersam').order_by("-dateTime")

    #Аналитик
    elif role['analyst']:
        samples = []
        if role['customer']:
            bsamples = Sample.objects.filter(customer=role['customer']).prefetch_related('ordersam').order_by("-dateTime")
            for sample in bsamples:
                if samples.count(sample) == 0:
                    samples.append(sample)
        orders = Order.objects.all().prefetch_related('analyst').filter(analyst__analyst=role['analyst']).order_by("dateTime")
        for order in orders:
            if samples.count(order.codeOfSample) == 0:
                samples.append(order.codeOfSample)
    #Заказчик
    elif role['customer']:
        #print(role['customer'])
        samples = Sample.objects.filter(customer=role['customer']).prefetch_related('ordersam').order_by("-dateTime")
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
    analysts = Analyst.objects.all()

    return render(request, 'analyzes/samples.html', {'page':page,
    'samples':samples,'atypes':atypes,'role':role, 'customers':customers,'analysts':analysts})


#===============================================================================
#
#
#===============================================================================
def list_types(request, samplepk):
    if samplepk is None:
        return
    error = None
    roles = getUserRole(request)

    analysts = Analyst.objects.all()
    print('analysts')
    print(analysts)

    if roles['customer'] is None:
        pass
    else:
        sample = Sample.objects.get(pk=samplepk)
        if sample.customer == roles['customer']:
            atypes = AnalyzeType.objects.all()
            atype = request.POST.getlist('atype',default=None)
            print(atype)
            projectpk = request.POST.get('project',default=None)
            if projectpk is None:
                project = None
            else:
                project =  Project.objects.get(pk=projectpk)
            if atype is None:
                orders = sample.ordersam.all()
                yettypes = []
                for order in orders:
                    yettypes.append(order.type.pk)

                for atype1 in atypes:
                    if atype1.pk in yettypes:
                        atype1.selected = "selected"
                    else:
                        atype1.selected = ""
            else:
                print("project = "+str(project))
                projects = Project.objects.all()
                #print(atype)
                #получаем все заказы для этого образца
                orders = sample.ordersam.all()
                yettypes = []
                for order in orders:
                    yettypes.append(order.type.pk)
                for atype1 in atypes:
                    if atype1.pk in yettypes:
                        atype1.selected = "selected"
                    else:
                        atype1.selected = ""
                for at in atype:
                    value = int(at)
                    if value in yettypes:
                        print('Уже есть '+str(value))
                        continue
                    #создать новый заказ
                    Order.objects.create(
                    code = getNewCodeOrder(),
                    codeOfSample=sample,
                    type=AnalyzeType.objects.get(pk=value),
                    customer=Customer.objects.get(person__user=roles['user']),
                    project=project,
                    executed=False
                    )
        else:
            atypes = []
            projects = []
            error="У Вас нет прав для правки чужих заявок."

    #добавить новый заказ к заказам
    orders = sample.ordersam.all()
    return render(request, 'analyzes/lt.html', {'sample':sample,'atypes':atypes,'orders':orders,'projects':projects,'analysts':analysts,'error':error})


def report(request):
    year = '2018'
    month='04'
    orders = Order.objects.filter(dateTime__year=year,dateTime__month=month).order_by('analyst__analyst','executed')
    #orders = Order.objects.filter(dateTime__year=year,dateTime__month=month)
    #orders = Order.objects.filter(dateTime__year=year,dateTime__month=month,executed=True)

    print(orders)
    massiv = {}
    analysts = {}
    customers = {}
    types = {}
    for order in orders:
        try:
            analyst = order.analyst.analyst
        except Exception as e:
            analyst  = None
        if (analyst,order.customer,order.type,order.executed) in massiv:
            massiv[(analyst,order.customer,order.type,order.executed)] += 1
        else:
            analysts[analyst]=True
            customers[order.customer]=True
            types[order.type]=True
            massiv[(analyst,order.customer,order.type,order.executed)] = 1
    print(analysts)
    print(customers)
    print(types)
    print(massiv)
    #убрать типы
    massivWithoutTypes={}
    for key in massiv:
        if (key[0],key[1],key[3]) in massivWithoutTypes:
            massivWithoutTypes[(key[0],key[1],key[3])] += massiv[key]
        else:
            massivWithoutTypes[(key[0],key[1],key[3])] = massiv[key]
    #print('massivWithoutTypes')
    #print(massivWithoutTypes)
    massivWithoutCustomer={}
    for key in massiv:
        if (key[0],key[2],key[3]) in massivWithoutCustomer:
            massivWithoutCustomer[(key[0],key[2],key[3])] += massiv[key]
        else:
            massivWithoutCustomer[(key[0],key[2],key[3])] = massiv[key]
    #print('massivWithoutCustomer')
    #print(massivWithoutCustomer)

    massivForHTML = []
    for key in massivWithoutCustomer:
        massivForHTML.append({'analyst':key[0],'type':key[1],'exectuted':key[2],
        'value':massivWithoutCustomer[key]})
    #print('massivForHTML')
    #print(massivForHTML)
    #analysts = []
    #counter1 = 0
    #lastanalyst = None
    #for order in orders:
    #    try:
    #        if order.analyst.analyst not in analysts:
    #            analysts.append(order.analyst.analyst)
    #            print (lastanalyst)
    #            print(counter1)
    #            lastanalyst = order.analyst.analyst
    #            counter1 = 1
    #        else:
    #            counter1+=1
    #    except Exception as e:
    #        pass
    #    else:
    #        print("---------")
    #        print(order)
    #        print(order.analyst.analyst)
    #        print("=========")
    #        pass

    #print (lastanalyst)
    #print(counter1)
    #print(analysts)
    reportName = "Имя отчета"
    table={}
    table['headers']=[]
    table['rows']=[]
    table['tails']=[]
    if len(request.POST):
        if request.POST.get('formsubmit', default=None):
            if request.POST.get('reporttype', default=None) == "1":
                analysts = []
                types = []
                for key in massivWithoutCustomer:
                    if key[2]:
                        if key[0] not in analysts:
                            analysts.append(key[0])
                        if key[1] not in types:
                            types.append(key[1])
                table['headers'].append({'name':"Метод\Измеритель"})
                for analyst in analysts:
                    table['headers'].append({'name':str(analyst)})
                for type1 in types:
                    tablerow = []
                    tablerow.append(str(type1))
                    for analyst in analysts:
                        try:
                            tablerow.append(massivWithoutCustomer[(analyst,type1,True)])
                        except Exception as e:
                            tablerow.append(0)
                    print(tablerow)
                    table['rows'].append(tablerow)
    print(table)
    return render(request, 'analyzes/report.html', {'reportName':reportName,'table':table})

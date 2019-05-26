from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
# Create your views here.
from modelapp.models import Book, Class, User


def homepage(request):
    newbook=Book.objects.all().order_by('-pub_time')[:8]
    goodbook=Book.objects.all().order_by('-print_count')[:10]
    nhotbook=Book.objects.all().order_by('-pub_time','-sales')[:5]
    orderto=request.GET.get('orderto')
    username=request.GET.get('username')
    hotbook=Book.objects.all().order_by('-sales')
    firstid=Class.objects.filter(level='1')
    secondid=Class.objects.filter(level='2')
    name = request.COOKIES.get('name')
    password = request.COOKIES.get('password')
    res=User.objects.filter(name=name,password=password)
    if orderto:
        a=request.session.get('usersname')
        if a:
            del request.session['usersname']
            del request.session['login']
        usersname=''
    elif username:
        usersname=username
    else:
        if res:
            usersname=name
        else:
            usersname = request.session.get('usersname')
    return render(request,'index.html',{'newbook':newbook,'goodbook':goodbook,'nhotbook':nhotbook,'hotbook':hotbook,'firstid':firstid,'secondid':secondid,'usersname':usersname})
def bookinfo(request):
    id = request.GET.get('id')
    request.session['bookid']=id
    book=Book.objects.filter(id=id)[0]
    cla=book.b_classid
    class2=cla.id
    a = request.session.get('usersname')
    if cla.id>15:
        class1 = Class.objects.filter(id=cla.first)[0]
    else:
        class1=''
    if cla.level==2:
        cla1=Class.objects.filter(id=cla.first)[0]
    else:
        cla1=Class.objects.filter(id=id)[0]
    pu=str(Book.objects.filter(id=id).values('pub_time')[0]['pub_time']).split('-')
    pr=str(Book.objects.filter(id=id).values('press_time')[0]['press_time']).split('-')
    press_time=str(pr[0])+'年'+str(pr[1])+'月'+str(pr[2])+'日'
    pub_time=str(pu[0])+'年'+str(pu[1])+'月'+str(pu[2])+'日'
    price=Book.objects.filter(id=id).values('price')[0]['price']
    ddprice = Book.objects.filter(id=id).values('ddprice')[0]['ddprice']
    d=(price/ddprice)*10
    discount=round(d,2)
    boook_dis=Book.objects.get(id=id)
    boook_dis.discount=discount
    boook_dis.save()
    return render(request,'Book details.html',{'book':book,'discount':discount,'pub_time':pub_time,'press_time':press_time,'cla1':cla1,'cla':cla,'class2':class2,'class1':class1,'a':a})
def bselect(request):
    a = request.session.get('usersname')
    opta=request.GET.get('opta')
    order=request.GET.get('tip')
    c_id=request.GET.get('cid')
    request.session['opta']=opta
    request.session['order']=order
    request.session['c_id']=c_id
    if c_id and c_id!='None':
        if int(c_id) > 15:
            s_class = Class.objects.filter(id=c_id)[0]
            f_class1=s_class.first
            f_class=Class.objects.filter(id=int(f_class1))[0]
        else:
            s_class = Class.objects.filter(id=c_id)[0]
            f_class = ''
    else:
        s_class=''
        f_class=''
    firstid = Class.objects.filter(level='1')
    secondid = Class.objects.filter(level='2')
    if c_id!="None" and c_id!=None:
        list1 = [int(c_id), ]
        if int(c_id) <= 15:
            order2 = Class.objects.filter(first=c_id).values('id')
            for i in order2:
                b = i['id']
                list1.append(b)
            t = tuple(list1)
            if order == '4' or opta=='sj':
                order1 = Book.objects.filter(b_classid__in=t).order_by('pub_time')
            elif order == '2' or opta=='xld':
                order1 = Book.objects.filter(b_classid__in=t).order_by('-sales')
            elif order == '3' or opta=='jgd':
                order1 = Book.objects.filter(b_classid__in=t).order_by('price')
            elif opta == 'xlu':
                order1 = Book.objects.filter(b_classid__in=t).order_by('sales')
            elif opta == "jgd":
                order1 = Book.objects.filter(b_classid__in=t).order_by('-price')
            else:
                order1 = Book.objects.filter(b_classid__in=t).order_by('b_name')
        else:
            if order == '4' or opta=='sj':
                order1 = Book.objects.filter(b_classid=c_id).order_by('pub_time')
            elif order == '2' or opta=='xlu':
                order1 = Book.objects.filter(b_classid=c_id).order_by('-sales')
            elif order == '3' or opta=='jgd':
                order1 = Book.objects.filter(b_classid=c_id).order_by('price')
            elif opta == 'xlu':
                order1 = Book.objects.filter(b_classid=c_id).order_by('sales')
            elif opta == "jgd":
                order1 = Book.objects.filter(b_classid=c_id).order_by('-price')
            else:
                order1 = Book.objects.filter(b_classid=c_id).order_by('b_name')
    else:
        if order == '4' or opta=='sj':
            order1 = Book.objects.all().order_by('pub_time')
        elif order == '2' or opta=='xld':
            order1 = Book.objects.all().order_by('-sales')
        elif order == '3' or opta=='jgu':
            order1 = Book.objects.all().order_by('price')
        elif opta=='xlu':
            order1=Book.objects.all().order_by('sales')
        elif opta=="jgd":
            order1=Book.objects.all().order_by('-price')
        else:
            order1 = Book.objects.all().order_by('b_name')
    number = request.GET.get('num')
    request.session['num'] = number
    if not number:
        number = 1
    pagtor = Paginator(order1,per_page=4)
    page=pagtor.page(number)
    sum=order1.count()
    return render(request,'booklist.html',{'firstid':firstid,'secondid':secondid,'order1':order1,'order':order,'c_id':c_id,"opta":opta,'page':page,'s_class':s_class,'f_class':f_class,'sum':sum,'a':a})

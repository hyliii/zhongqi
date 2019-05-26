import random
import string

from django.core.serializers import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from carapp.car import Cartltem, Cart
from modelapp.models import Book, User, Address, Order, Orders


def carview(request):
    cart=request.session.get('cart')
    a = request.session.get('usersname')
    if cart is None:
        return render(request,'car.html',{'total_price':0,'sum_price':0,'a':a})
    c_book=cart.cartltems
    d_book=cart.dustbin
    sum_amount=cart.sum_amount
    cart.c_sums()
    sum_price=cart.sum_price
    total_price=cart.total_price
    return render(request,'car.html',{'c_book':c_book,'total_price':total_price,'sum_price':sum_price,'d_book':d_book,'a':a,'sum_amount':sum_amount})
def addajax(request):
    b_id=int(request.GET.get('b_id'))
    amount1=int(request.GET.get('amount'))
    cart=request.session.get('cart')
    if cart is None:
       cart=Cart()
       cart.c_add(b_id,amount1)
       request.session['cart'] = cart
    else:
        cart.c_add(b_id,amount1)
        request.session['cart'] = cart
    return HttpResponse('1')
def updateajax(request):
    b_id = int(request.GET.get('b_id'))
    amount1 = int(request.GET.get('amount'))
    cart = request.session.get('cart')
    cart.c_update(b_id,amount1)
    cart.c_sums()
    sums=cart.sum_price
    total=cart.total_price
    request.session['cart'] = cart
    return HttpResponse(str(sums)+'+'+str(total))
def removeajax(request):
    order=request.GET.get('order')
    b_id=int(request.GET.get('b_id'))
    amount1 = request.GET.get('amount')
    cart=request.session.get('cart')
    cart.c_remove(b_id,order,amount1)
    request.session['cart'] = cart
    return HttpResponse('1')
def recoverajax(request):
    order=request.GET.get('order')
    b_id=int(request.GET.get('b_id'))
    amount1 = request.GET.get('amount')
    cart=request.session.get('cart')
    cart.c_recover(b_id,order,amount1)
    request.session['cart'] = cart
    return HttpResponse('1')
def pay(request):
    loginflag=request.session.get('login')
    if loginflag=='ok':
        usersname=request.session.get('usersname')
        u_id=User.objects.filter(name=usersname).values('id')[0]['id']
        addres=Address.objects.filter(user_id=u_id)
        cart=request.session.get('cart')
        if cart is None:
            return render(request,'indent.html',{'usersname':usersname,'addres':addres,'sum_price':0,'total_price':0})
        else:
            c_book = cart.cartltems
            cart.c_sums()
            sum_price = cart.sum_price
            total_price = cart.total_price
            p_price=cart.p_price
            return render(request,'indent.html',{'usersname':usersname,'addres':addres,'c_book':c_book,'sum_price':sum_price,'total_price':total_price,'p_price':p_price})
    else:
        return redirect('user:login')
def buyajax(request):
    cart = request.session.get('cart')
    if cart:
        cartltems = cart.cartltems
        if cartltems==[]:
            return HttpResponse('0')
        else:
            return HttpResponse('1')
    else:
        return HttpResponse('0')

def payajax(request):
    ad_id=request.GET.get('ad_id')
    address = Address.objects.filter(id=int(ad_id))
    def address_default(a):
        if isinstance(a,Address):
            return {'id':a.id,'person':a.person,'address':a.address,'postal_code':a.postal_code,'phone':a.phone,'tel':a.tel,'user_id':a.user_id}
    return JsonResponse(list(address),safe=False,json_dumps_params={'default':address_default})
def referok(request):
    cart = request.session.get('cart')
    paybox1=request.session.get('paybox')
    loginflag = request.session.get('login')
    user_name = request.GET.get('user_name')
    addresss = request.GET.get('addresss')
    post_code = request.GET.get('post_code')
    phonenumber = request.GET.get('phonenumber')
    telnumber = request.GET.get('telnumber')
    dict1=request.session.get('dict1')
    if loginflag == 'ok':
        numb=random.sample(string.digits,10)
        r_numb=''.join(numb)
        request.session['r_numb']=r_numb
        usersname = request.session.get('usersname')
        username_id=User.objects.filter(name=usersname).values('id')[0]['id']
        sum_amount=cart.sum_amount
        Order.objects.create(address=dict1['addresss'],order_id=r_numb,user_id_id=username_id)
        order=Order.objects.filter(order_id=r_numb)[0]
        for i in paybox1:
            bookprice=i.book.price
            bookid=i.book.id
            num=i.amount
            sum=int(bookprice)*int(num)
            order.orders_set.create(sum=sum,goods_id_id=bookid,order_id=order.id,goods_num=num)
        if user_name is None or addresss is None or post_code is None or phonenumber is None and telnumber is None:
            return render(request, 'indent ok.html', {'usersname': usersname,'r_numb':r_numb,'sum':sum,'sum_amount':sum_amount,'user_name':dict1['user_name'],'addresss':dict1['addresss'],'post_code':dict1['post_code'],'tel':dict1['telture']})
        else:
            Address.objects.create(person=user_name,address=addresss,postal_code=post_code,phone=phonenumber,tel=telnumber,user_id_id=username_id)
            return render(request,'indent ok.html',{'usersname':usersname,'r_numb':r_numb,'sum_amount':sum_amount,'sum':sum,'user_name':dict1['user_name'],'addresss':dict1['addresss'],'post_code':dict1['post_code'],'tel':dict1['telture']})
    else:
        return redirect('user:login')
def referajax(request):
    user_name=request.GET.get('user_name')
    addresss=request.GET.get('addresss')
    post_code=request.GET.get('post_code')
    phonenumber=request.GET.get('phonenumber')
    telnumber=request.GET.get('telnumber')
    cart = request.session.get('cart')
    cartltems=cart.cartltems
    paybox1=[]
    if user_name=='' or addresss=='' or post_code=='' or phonenumber=='' and telnumber=='':
        return HttpResponse('0')
    else:
        if telnumber=='':
            telture=phonenumber
        else:
            telture=telnumber
        dict1 = {'user_name': user_name, 'addresss': addresss, 'post_code': post_code, 'telture':telture}
        request.session['dict1'] = dict1
        paybox1.extend(cartltems)
        request.session['paybox']=paybox1
        cartltems.clear()
        request.session['cart']=cart
        return HttpResponse('1')
import hashlib
import random
import string
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse

# Create your views here.
from modelapp.models import User, Address
from userapp.captcha.image import ImageCaptcha
from zhongqi import settings



def send_email(request):
    user_email=request.GET.get('user_email')
    code1=request.session.get('code1')
    subject = 'hyl验证码'
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，您的验证码是{}'.format(code1)
    html_content = '<p>{}感谢注册<a href="http://{}/userapp/youxiang/?email={}" onclink="user_check()">< / a >欢迎你来验证你的邮箱，点一下你就可以成功注册了！ < / p > '.format(user_email,'127.0.0.1:8000', user_email)
    msg = EmailMultiAlternatives(subject, text_content, 'hyl_t@sina.com',  [user_email])
    # 发送的heml文本的内容
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse('1')

def youxiang(request):
    email=request.GET.get('email')
    request.session['email1']=email
    return render(request,'youxiang.html',{'email':email})
def regist(request):
    return render(request,'register.html')
def getcaptcha(request):
    image=ImageCaptcha()
    code=random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,1)
    r_code=''.join(code)
    request.session['code']=r_code
    data=image.generate(r_code)
    return HttpResponse(data,'image/png')
def getcaptcha2(request):
    image=ImageCaptcha()
    code1=random.sample(string.digits,2)
    r_code1=''.join(code1)
    request.session['code1']=r_code1
    data=image.generate(r_code1)
    return HttpResponse(data,'image/png')
def youxiangajax(request):
    if request.method=="POST":
        code1=request.POST.get('code')
        code=request.session.get('code1')
        if code.upper() == code1.upper():
            return HttpResponse('1')
        else:
            return HttpResponse('0')
def reajaxlogic(request):
    if request.method=="POST":
        code1=request.POST.get('code')
        code=request.session.get('code')
        if code.upper() == code1.upper():
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        name = request.GET.get('name')
        print(name)
        res = User.objects.filter(name=name)
        if res:
            return HttpResponse('0')
        else:
            return HttpResponse('1')
def coajax(request):
    code1 = request.GET.get('code')
    code = request.session.get('code1')
    if code1.upper()==code.upper():
        return HttpResponse('1')
    else:
        return HttpResponse('0')
def email_check(request):
    email=request.session.get('email1')
    code=request.GET.get('txt_vcode')
    dict2=request.session.get('dict2')
    name=dict2['name']
    if code:
        user=User.objects.filter(email=email,name=name)[0]
        user.has_comfire=True
        user.save()
        return render(request, 'register ok.html', {'name': email})
    else:
        return  HttpResponse('<script>if (window.confirm("邮箱验证未完成,确定要登陆？")){window.location.href="http://127.0.0.1:8000/userapp/login"}else{window.location.href="http://127.0.0.1:8000/informationapp/homepage"}</script>')

def nacoajax(request):
    code1=request.GET.get('code')
    code=request.session.get('code')
    name = request.GET.get('name')
    res = User.objects.filter(name=name)
    if not res and code1.upper()==code.upper():
        return HttpResponse('1')
    else:
        return HttpResponse('0')
def registlogic(request):
    try:
        with transaction.atomic():
            name = request.POST.get('txt_username')
            password = request.POST.get('txt_password')
            passwordm=hashlib.md5()
            passwordm.update(password.encode())
            passwords=passwordm.hexdigest()
            email=request.POST.get('txt_usernamee')
            dict2={'name':name,'email':email}
            request.session['dict2']=dict2
            User.objects.create(name=name,email=email, password=passwords)
            request.session['usename']=name
            has_comfire=User.objects.filter(email=email,name=name).values('has_comfire')[0]['has_comfire']
            if has_comfire:
                return render(request,'register ok.html',{'name':name})
            else:
                return HttpResponse('<script>if (window.confirm("邮箱还未验证，先前往首页么？")){window.location.href="http://127.0.0.1:8000/informationapp/homepage"}else{window.location.href="http://127.0.0.1:8000/userapp/login"}</script>')
    except:
        return HttpResponse('<script>if (window.confirm("发生错误，是否继续？")){window.location.href="http://127.0.0.1:8000/userapp/regist"}else{window.location.href="http://127.0.0.1:8000/informationapp/homepage"}</script>')
def login(request):
    name = request.COOKIES.get('name')
    password = request.COOKIES.get('password')
    orderto = request.GET.get('orderto')
    request.session['orderto'] = orderto
    if password:
        passwordm = hashlib.md5()
        passwordm.update(password.encode())
        passwords = passwordm.hexdigest()
        result = User.objects.filter(name=name, password=passwords)
        if result:
            request.session['login'] = 'ok'
            return redirect('information:homepage')
    else:
        return render(request, 'login.html')
def loginajax(request):
    code=request.POST.get('code1')
    recode=request.session.get('code')
    usersname=request.POST.get('usersname')
    password=request.POST.get('password')
    passwordm = hashlib.md5()
    passwordm.update(password.encode())
    passwords = passwordm.hexdigest()
    res=User.objects.filter(name=usersname,password=passwords)
    has_comfire = User.objects.filter( name=usersname).values('has_comfire')[0]['has_comfire']
    if res and recode.upper()==code.upper():
        if has_comfire:
            request.session['usersname'] = usersname
            request.session['login'] = 'ok'
        return HttpResponse('1')
    else:
        return HttpResponse('0')
def loginlogic(request):
    usersname=request.POST.get('txtUsername')
    password=request.POST.get('txtPassword')
    passwordm = hashlib.md5()
    passwordm.update(password.encode())
    passwords = passwordm.hexdigest()
    rem = request.POST.get('autologin111')
    resto =redirect('information:homepage')
    has_comfire = User.objects.filter(name=usersname).values('has_comfire')[0]['has_comfire']
    if has_comfire:
        if rem == '1':
            resto.set_cookie('name', usersname, max_age=7 * 24 * 3600)
            resto.set_cookie('password', passwords, max_age=7 * 24 * 3600)
        cart = request.session.get('cart')
        orderto=request.session.get('orderto')
        if orderto=='1':
            return resto
        if orderto=='2':
            id=request.session.get('bookid')
            url=reverse('information:bookinfo')+'?id='+str(id)
            return redirect(url)
        if orderto=='3':
            c_id=request.session.get('c_id')
            opta=request.session.get('opta')
            order=request.session.get('order')
            url=reverse('information:bselect')+'?c_id='+str(c_id)+'&opta='+str(opta)+'&order='+str(order)
            return redirect(url)
        if orderto=='4':
            return redirect('carapp:carview')
        if cart :
            u_id = User.objects.filter(name=usersname).values('id')[0]['id']
            addres = Address.objects.filter(user_id=u_id)
            c_book = cart.cartltems
            cart.c_sums()
            sum_price = cart.sum_price
            total_price = cart.total_price
            return render(request, 'indent.html', {'usersname': usersname, 'addres': addres, 'c_book': c_book, 'sum_price': sum_price,'total_price': total_price})
        return resto
    else:
        return HttpResponse('<script>if (window.confirm("邮箱还未验证，先前往首页么？")){window.location.href="http://127.0.0.1:8000/informationapp/homepage"}else{window.location.href="http://127.0.0.1:8000/userapp/login"}</script>')


def sessionajax(request):
    del request.session['usersname']
    return HttpResponse('1')

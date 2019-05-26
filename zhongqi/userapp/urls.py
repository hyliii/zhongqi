from django.urls import path, include

from userapp import views
app_name='user'
urlpatterns = [
    path('regist/',views.regist,name='regist'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('reajaxlogic/',views.reajaxlogic,name='reajaxlogic'),
    path('registlogic/',views.registlogic,name='registlogic'),
    path('nacoajax/',views.nacoajax,name='nacoajax'),
    path('login/',views.login,name='login'),
    path('loginajax/',views.loginajax,name='loginajax'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('sessionajax/',views.sessionajax,name='sessionajax'),
    path('send_email/',views.send_email,name='send_email'),
    path('youxiang/',views.youxiang,name='youxiang'),
    path('youxiangajax/',views.youxiangajax,name='youxiangajax'),
    path('getcaptcha2/',views.getcaptcha2,name='getcaptcha2'),
    path('coajax/',views.coajax,name='coajax'),
    path('email_check/',views.email_check,name='email_check'),




]
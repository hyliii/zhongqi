from carapp import views
from django.urls import path
app_name='carapp'
urlpatterns = [
        path('carview/',views.carview,name='carview'),
        path('addajax/',views.addajax,name='addajax'),
        path('updateajax/',views.updateajax,name='updateajax'),
        path('removeajax/',views.removeajax,name='removeajax'),
        path('recoverajax/',views.recoverajax,name='recoverajax'),
        path('pay/',views.pay,name='pay'),
        path('payajax/',views.payajax,name='payajax'),
        path('referok/',views.referok,name='referok'),
        path('referajax/',views.referajax,name='referajax'),
        path('buyajax/',views.buyajax,name='buyajax')
    ]
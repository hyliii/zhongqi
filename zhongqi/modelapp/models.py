from django.db import models

# Create your models here.
class User(models.Model):
    email=models.CharField(max_length=40)
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=100)
    c_time=models.DateTimeField (auto_now_add=True,null=True,blank=True)
    has_comfire=models.BooleanField(default=False,blank=True)
class Order(models.Model):
    user_id=models.ForeignKey(to=User,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=40)
    order_time=models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=100)
class Class(models.Model):
    classify=models.CharField(max_length=20)
    level=models.IntegerField()
    first=models.IntegerField(null=True)
    second=models.IntegerField(null=True)
class Book(models.Model):
    b_name=models.CharField(max_length=40)
    series_name=models.CharField(max_length=80)
    writer=models.CharField(max_length=20)
    publisher=models.CharField(max_length=80)
    press_time=models.CharField(max_length=40)
    price=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    ddprice=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    press_count=models.CharField(max_length=20)
    print_count=models.IntegerField()
    inter_num=models.CharField(max_length=20)
    b_class=models.CharField(max_length=20)
    word_num=models.CharField(max_length=20)
    page_num=models.CharField(max_length=20)
    format=models.CharField(max_length=20)
    pack=models.CharField(max_length=20)
    pub_time=models.DateField()
    sales=models.IntegerField()
    discuss_count=models.IntegerField(null=True)
    b_classid=models.ForeignKey(to=Class,on_delete=models.CASCADE)
    pics=models.ImageField(upload_to="pics", null=True,blank=True)
    discount=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
class Orders(models.Model):
    goods_id=models.ForeignKey(to=Book,on_delete=models.CASCADE)
    goods_num=models.IntegerField( null=True,blank=True)
    order_id=models.ForeignKey(to=Order,on_delete=models.CASCADE)
    sum=models.FloatField()
class Address(models.Model):
    person=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=10)
    phone=models.CharField(max_length=20,null=True)
    tel=models.CharField(max_length=20,null=True)
    user_id=models.ForeignKey(to=User,on_delete=models.CASCADE)
class Tcode(models.Model):
    code=models.CharField(max_length=20)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    code_time=models.DateTimeField(auto_now_add=True)


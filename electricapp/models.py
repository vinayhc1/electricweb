from django.db import models

# Create your models here.

class Customer(models.Model):
   name = models.CharField(max_length=50)
   email = models.EmailField()
   phone = models.IntegerField()
   address = models.TextField(default='None')
    
class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    payperday = models.IntegerField()
    advance = models.IntegerField()

class Brand(models.Model):
    name = models.CharField(max_length=50)

class ItemType(models.Model):
    type = models.CharField(max_length=50)
    
class Item(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.IntegerField()

class Attendance(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=2, decimal_places=1)
    pay = models.IntegerField()

class MatList(models.Model):
    customer = models.CharField(max_length = 50)
    item = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()

class Etransaction(models.Model):
    employee = models.CharField(max_length=50)
    month = models.IntegerField()
    year = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    pay = models.IntegerField()

class Ctransaction(models.Model):
    customer = models.CharField(max_length=50)
    month = models.IntegerField()
    year = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    pay = models.IntegerField()


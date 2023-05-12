from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse 
from django.contrib import messages
from electricapp.models import *
from django.utils.timezone import localdate
from django.db.models import Sum    
# Create your views here.

#PDF imports
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from html import escape
from io import BytesIO


def index(request):
    return render(request, "index.html")

def attendance(request):
     if request.method=='POST':
       name = request.POST['name']
       date = request.POST['date']
       value = request.POST['value']
       if name == 'Select Employee':
         messages.error(request,"Select Employee")
         return redirect('/attendance')
       if value == '0':
         messages.error(request,"Value cannot be 0")
         return redirect('/attendance')
       if date > str(localdate()):
          messages.error(request,"Cannot Add for Future Dates")
          return redirect('/attendance')
       pay = float(value) * Employee.objects.filter(name = name).aggregate(Sum('payperday'))['payperday__sum']
       obj, created = Attendance.objects.update_or_create(
          name = name,
          date = date,
          defaults={'value': value, 'pay' : pay}
       )
       messages.success(request,"Attendance Added Successfully")
       return redirect('/attendance') 
     elif request.method=='GET':
       employees = Employee.objects.all()
       data = {
        'employees': employees
       }
     return render(request, "attendance.html",data) 

def mat_list(request):
    if request.method == 'POST':
       cust = request.POST['name']
       type = request.POST['type']
       items = Item.objects.filter(type=type)
       matlist = MatList.objects.filter(customer = cust, type = type)
       data = {
          'items': items,
          'matlist': matlist,
          'type': type,
          'cust':cust
       }
       return render(request,"mat_list.html",data)
    elif request.method=='GET':
      customers = Customer.objects.all()
      itemtypes = ItemType.objects.all()
      data = {
        'customers': customers,
        'itemtypes': itemtypes
    }
    return render(request,"mat_list.html",data)

def c_billing(request):
    if request.method == 'GET':
      customers = Customer.objects.all()
      itemtypes = ItemType.objects.all()
      data = {
        'customers': customers,
        'itemtypes': itemtypes }
      return render(request, "c_billing.html", data)
    elif request.method == 'POST':
       customer = request.POST['customer']
       type = request.POST['type']
       if  customer == 'Select Customer':
             messages.error(request,"Select Customer to proceed")
             return redirect('/c_billing')
       elif type == 'Select Item Type':
             messages.error(request,"Select Item Type to proceed")
             return redirect('/c_billing')
       if request.POST['price'] != '':
         item = request.POST['item']
         brand = request.POST['brand']
         quantity = request.POST['quantity']
         price = int(quantity) * int(request.POST['price'])
         obj, created = MatList.objects.update_or_create(
           customer = customer,
           item = item,
           brand = brand,
           defaults= {'quantity': quantity, 'price': price }
          )
       if request.POST['labour'] != '':
         ltype = request.POST['ltype']
         labour = int(request.POST['labour'])
         q = 1
         obj, created = MatList.objects.update_or_create(
           customer = customer,
           type = ltype,
           quantity = q,
           defaults= {'price': labour }
          )
       if request.POST['lpay'] != '':
          date= str(localdate())
          month = int(date[5:7])
          year = int(date[0:4])
          myquery = Ctransaction(customer = customer, month = month, year = year, date = date, pay = int(request.POST['lpay']) )
          myquery.save()
       if type == 'All':
         matlist = MatList.objects.filter(customer = customer, price = 0).exclude(type = 'Labour')
         mprice = MatList.objects.filter(customer = customer).exclude(price = 0).exclude(type = 'Labour')
       else:
         matlist = MatList.objects.filter(customer = customer, type = type, price = 0).exclude(type = 'Labour')
         mprice = MatList.objects.filter(customer = customer, type = type).exclude(price = 0).exclude(type = 'Labour')
       mptotal =  mprice.aggregate(Sum('price'))['price__sum']
       if mptotal is None:
         mptotal = 0
       labourc = MatList.objects.filter(customer = customer, type = 'Labour').aggregate(Sum('price'))['price__sum']
       if labourc is None:
          labourc = 0
       gtotal = labourc + mptotal
       lpayment = Ctransaction.objects.filter(customer = customer).aggregate(Sum('pay'))['pay__sum']
       if lpayment is None:
          lpayment = 0
       data = {
         'matlist' : matlist,
         'mprice' : mprice,
         'cust': customer,
         'type': type,
         'mptotal': mptotal,
         'labourc': labourc,
         'gtotal': gtotal,
         'lpayment': lpayment,
      }
       return render(request, "c_billing.html", data)
          
       

def e_billing(request):
    if request.method=='GET':
       employees = Employee.objects.all()
       data = {
          'employees': employees
       }
       return render(request, "e_billing.html",data)
    elif request.method == 'POST':
       name = request.POST['name']
       date= str(localdate())
       month = int(date[5:7])
       year = int(date[0:4])
       months  = { '1' : 'January' , '2': 'February' , '3': 'March', '4': 'April',
                   '5': 'May', '6': 'June', '7': 'July', '8': 'August',
                   '9': 'September', '10': 'October', '11': 'November' , '12': 'December'}
       if name == 'Select Employee':
          messages.error(request,"Select Employee to proceed")
          return redirect('/e_billing')
       if name != 'Select Employee' and request.POST['month'] != '' and request.POST['year'] != '':
          if  request.POST['month'] == 'Select month':
             messages.error(request,"Select month to proceed")
          elif request.POST['year'] == 'Select Year':
             messages.error(request,"Select Year to proceed")
          elif ( int(request.POST['month']) > month ) and ( int(request.POST['year']) >= year) :
             messages.error(request,"Cannot Add for future dates")
          else:
             old_amount = Etransaction.objects.filter(month = int(request.POST['month']), year  = int(request.POST['year']), employee = name).aggregate(Sum('pay'))['pay__sum']
             if old_amount is not None:
                full_amount = old_amount + int(request.POST['amount'])
             else:
                full_amount = int(request.POST['amount'])
             n_year = request.POST['year'] + '-' + request.POST['month']
             tot_amount = Attendance.objects.filter(date__startswith = n_year, name = name).aggregate(Sum('pay'))['pay__sum']
             if tot_amount is not None and tot_amount < full_amount :
                err_message = str(request.POST['amount']) + '+' + str(old_amount) + " exceeds actual pay of " + str(tot_amount)
                messages.error(request,err_message)
             else:
                   myquery = Etransaction(employee = name, month = int(request.POST['month']), year = int(request.POST['year']),
                                          date = localdate()  , pay = int(request.POST['amount']) )
                   myquery.save()  
       count = 0
       flag = 0
       while count < 7:
          if month == 0:
             month = 12
             year = year - 1
          if len(str(month)) != 2:
             m_year = str(year) + '-' + '0' + str(month)
          else:
             m_year = str(year) + '-' + str(month)
          if count == 0:
             current_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))['pay__sum']
             current_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
             if current_pay is not None and current_paid is not None:
               current_pper = ( current_paid * 100 ) / current_pay
             elif current_pay is None:
               current_pay = 0
               current_paid = 0
               current_pper = 0
             elif current_paid is None:
               current_paid = 0
               current_pper = 0
             current_month = months[str(month)]
          elif count == 1:
             second_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))['pay__sum']
             second_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
             if second_pay is not None and second_paid is not None:
               second_pper = ( second_paid * 100 ) / second_pay
             elif second_pay is None:
               second_pay = 0
               second_paid = 0
               second_pper = 0
             elif second_paid is None:
                second_paid = 0
                second_pper = 0
             second_month = months[str(month)]
          elif count == 2:
             third_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))['pay__sum']
             third_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
             if third_pay is not None and third_paid is not None:
               third_pper = ( third_paid * 100 ) / third_pay
             elif third_pay is None:
                third_pay = 0
                third_paid = 0
                third_pper = 0
             elif third_paid is None:
                third_paid = 0
                third_pper = 0
             third_month = months[str(month)]
          elif count == 3:
             fourth_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))['pay__sum']
             fourth_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
             if fourth_paid is not None and fourth_pay is not None:
                fourth_pper = ( fourth_paid * 100 ) / fourth_pay
             elif fourth_pay is None:
                fourth_pay = 0
                fourth_paid = 0
                fourth_pper = 0
             elif fourth_paid is None:
                fourth_paid = 0
                fourth_pper = 0
             fourth_month = months[str(month)]
          elif count == 4:
             fifth_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))['pay__sum']
             fifth_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
             if fifth_paid is not None and fifth_pay is not None:
               fifth_pper = ( fifth_paid * 100 ) / fifth_pay
             elif fifth_pay is None:
                fifth_pay = 0
                fifth_paid = 0
                fifth_pper = 0
             elif fifth_paid is None:
                fifth_paid = 0
                fifth_pper = 0
             fifth_month = months[str(month)]
          elif count == 5:
             sixth_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))['pay__sum']
             sixth_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
             if sixth_paid is not None and sixth_pay is not None:
               sixth_pper = ( sixth_paid * 100 ) / sixth_pay
             elif sixth_pay is None:
                sixth_pay = 0
                sixth_paid = 0
                sixth_pper = 0
             elif sixth_paid is None:
                sixth_paid = 0
                sixth_pper = 0
             sixth_month = months[str(month)]
          count = count + 1
          month = month - 1
       if current_pay or second_pay or third_pay or fourth_pay  or fifth_pay or sixth_pay :
            flag = 1
       advance = Employee.objects.filter(name = name).aggregate(Sum('advance'))['advance__sum']
       data = {
          'flag': flag,
          'current_pay': current_pay,
          'second_pay' : second_pay,
          'third_pay' : third_pay ,
          'fourth_pay' : fourth_pay ,
          'fifth_pay' : fifth_pay,
          'sixth_pay' : sixth_pay,
          'current_paid': current_paid,
          'second_paid' : second_paid,
          'third_paid' : third_paid ,
          'fourth_paid' : fourth_paid ,
          'fifth_paid' : fifth_paid,
          'sixth_paid' : sixth_paid,
          'current_pper': current_pper,
          'second_pper' : second_pper,
          'third_pper' : third_pper ,
          'fourth_pper' : fourth_pper ,
          'fifth_pper' : fifth_pper,
          'sixth_pper' : sixth_pper,
          'current_month': current_month,
          'second_month' : second_month,
          'third_month' : third_month ,
          'fourth_month' : fourth_month ,
          'fifth_month' : fifth_month,
          'sixth_month' : sixth_month,
          'employee': name,
          'advance': advance,
           
       }
       return render(request, "e_billing.html",data)

def local_admin(request):
    return render(request, "local_admin.html")

def add_employee(request):
    if request.method=='POST':
      username = request.POST['name']
      emailid = request.POST['email']
      phone = request.POST['phone']
      pay = request.POST['pay']
      advance = request.POST['advance']
      if len(phone) != 10  :
         messages.error(request,"Invalid Phone Number")
         return redirect('/add_employee')
      empl = Employee.objects.all()
      for e in empl:
        if e.name == username:
          messages.error(request,"User Already exists")
          return redirect('/add_employee')
      myquery = Employee(name = username,email = emailid,phone = phone,payperday = pay, advance = advance)
      myquery.save()
      messages.success(request,"Employee Added Successfully")
      return render(request,"add_employee.html")
    return render(request,"add_employee.html")

def update_employee(request):
    if request.method=='POST':
        id = request.POST['id']
        emailid = request.POST['email']
        phone = request.POST['phone']
        pay = request.POST['pay']
        advance = request.POST['advance']
        if len(phone) != 10  :
          messages.error(request,"Invalid Phone Number")
          return redirect('/manage_employees') 
        myquery = Employee.objects.get(id=id)
        myquery.email = emailid
        myquery.phone = phone
        myquery.payperday = pay
        myquery.advance = advance
        myquery.save()
        messages.success(request,"Employee Updated Successfully")
        return redirect('/manage_employees')  

def delete_employee(request):
    if request.method=='POST':
      id = request.POST['id']
      myquery = Employee.objects.get(id=id)
      del_att = Attendance.objects.filter(name = myquery.name)
      del_att.delete()
      myquery.delete()
      messages.success(request,"Employee Deleted Successfully")
      return redirect('/manage_employees')

def add_item(request):
    if request.method=='POST':
       name = request.POST['name']
       type = request.POST['type']
       brand = request.POST['brand']
       price = request.POST['price']
       if type == ''  :
          messages.error(request,"Please select Item Type")
          return redirect('/add_item')
       #myquery = Item(name = name, type = type,price = price)
       obj, created = Item.objects.update_or_create(
          name = name,
          type = type,
          brand = brand,
          defaults={'price': price }
       )
       #myquery.save()
       messages.success(request,"Item Added Successfully")
       return redirect('/add_item') 
    elif request.method=='GET':
       itemtype = ItemType.objects.all()
       brand = Brand.objects.all()
    data = {
          'itemtypes': itemtype,
          'brands': brand
    }
    return render(request, "add_item.html",data)

def manage_itemtype(request):
    if request.method=='GET':
       itemtype = ItemType.objects.all()
    data = {
          'itemtypes': itemtype
    }
    return render(request, "manage_itemtype.html",data)

def add_itemtype(request):
    if request.method=='POST':
       type = request.POST['type']
       myquery = ItemType(type = type)
       myquery.save()
       messages.success(request,"Item Type Added Successfully")
       return redirect('/manage_itemtype') 
    return render(request, "manage_itemtype.html")

def delete_itemtype(request):
    if request.method=='POST':
      id = request.POST['id']
      myquery = ItemType.objects.get(id=id)
      todelete = Item.objects.filter(type=myquery.type)
      todelete.delete()
      myquery.delete()
      messages.success(request,"Item Type & Its Items Deleted Successfully")
      return redirect('/manage_itemtype')
    return render(request, "manage_itemtype.html")


def manage_employees(request):
   if request.method=='GET':
      employees = Employee.objects.all()
      data = {
        'employees': employees
    }
   return render(request,"manage_employees.html",data)

def att_report(request):
   if request.method =='POST':
      month = request.POST['month']
      year = request.POST['year']
      name = request.POST['name']
      m_year = year + '-' + month
      employees = Employee.objects.all()
      attendance = Attendance.objects.filter(date__startswith = m_year, name = name)
      total_days = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('value'))
      total_pay = Attendance.objects.filter(date__startswith = m_year, name = name).aggregate(Sum('pay'))
      data = {
          'employees': employees,
          'name': name,
          'month': month,
          'year': year,
          'attendance': attendance,
          'total': total_days['value__sum'],
          'pay': total_pay['pay__sum']
      }
      return render(request, "att_report.html",data)
   elif request.method =='GET':
      employees = Employee.objects.all()
      data = {
         'employees': employees
      }
      return render(request, "att_report.html",data)

def add_customer(request):
    if request.method=='POST':
      username = request.POST['name']
      emailid = request.POST['email']
      phone = request.POST['phone']
      address = request.POST['address']
      if len(phone) != 10  :
         messages.error(request,"Invalid Phone Number")
         return redirect('/add_customer')
      cust = Customer.objects.all()
      for c in cust:
        if c.name == username:
          messages.error(request,"Customer Already exists")
          return redirect('/add_customer')
      myquery = Customer(name = username,email = emailid,phone = phone,address = address)
      myquery.save()
      messages.success(request,"Customer created Successfully")
      return render(request,"add_customer.html")
    return render(request,"add_customer.html")

def manage_customers(request):
   if request.method=='GET':
      customers = Customer.objects.all()
      data = {
        'customers': customers
    }
   return render(request,"manage_customers.html",data)

def update_customer(request):
    if request.method=='POST':
        id = request.POST['id']
        emailid = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        if len(phone) != 10  :
          messages.error(request,"Invalid Phone Number")
          return redirect('/manage_customers')  
        myquery = Customer.objects.get(id=id)
        myquery.email = emailid
        myquery.phone = phone
        myquery.address = address
        myquery.save()
        messages.success(request,"Customer Updated Successfully")
        return redirect('/manage_customers')  

def delete_customer(request):
    if request.method=='POST':
      id = request.POST['id']
      myquery = Customer.objects.get(id=id)
      myquery.delete()
      messages.success(request,"Customer Deleted Successfully")
      return redirect('/manage_customers')

def manage_items(request):
   if request.method=='GET':
      items = Item.objects.all()
      itemtypes = ItemType.objects.all()
      brand = Brand.objects.all()
      data = {
        'items': items,
        'itemtypes': itemtypes,
        'brands': brand,
    }
   return render(request,"manage_items.html",data)

def update_item(request):
    if request.method=='POST':
        id = request.POST['id']
        type = request.POST['type']
        brand = request.POST['brand']
        price = request.POST['price']
        myquery = Item.objects.get(id=id)
        myquery.price = price
        myquery.type = type
        myquery.brand = brand
        myquery.save()
        messages.success(request,"Item Updated Successfully")
        return redirect('/manage_items') 

def delete_item(request):
    if request.method=='POST':
      id = request.POST['id']
      myquery = Item.objects.get(id=id)
      myquery.delete()
      messages.success(request,"Item Deleted Successfully")
      return redirect('/manage_items')
    
def add_material(request):
    if request.method =='POST':
       customer = request.POST['customer']
       item = request.POST['item']
       quantity = request.POST['quantity']
       type = request.POST['type']
       brand = request.POST['brand']
       if quantity != '0':
         #myquery = MatList(customer = customer, item = item, quantity = quantity, type = type, brand = brand)
         obj, created = MatList.objects.update_or_create(
           customer = customer,
           item = item,
           type = type,
           brand = brand,
           defaults={'quantity': quantity}
          )
    items = Item.objects.filter(type=type)
    matlist = MatList.objects.filter(customer = customer, type = type)
    data = {
      'items': items,
      'matlist': matlist,
      'type': type,
      'cust':customer
        }
    return render(request,"mat_list.html",data)
    

def delete_material(request):
   if request.method == 'POST':
      customer = request.POST['customer']
      type = request.POST['type']
      id = request.POST['id']
      myquery = MatList.objects.get(id = id)
      myquery.delete()
      items = Item.objects.filter(type=type)
      matlist = MatList.objects.filter(customer = customer, type = type)
      data = {
          'items': items,
          'matlist': matlist,
          'type': type,
          'cust':customer
      }
      return render(request,"mat_list.html",data)

def new_material(request):
    return redirect('/mat_list')

def print_list(request):
    if request.method =='POST':
      pass
    elif request.method =='GET':
       customers = Customer.objects.all()
       itemtypes = ItemType.objects.all()
       data = {
         'customers': customers,
         'itemtypes': itemtypes
       }  
       return render(request, "print_list.html", data)

def get_list(request):
   if request.method == 'POST':
      cust = request.POST['name']
      type = request.POST['type']
      if cust == 'Select Customer':
         messages.error(request,"Select Customer")
         return redirect('/print_list')
      
      if type == 'Select Item Type':
         messages.error(request,"Select Item Type")
         return redirect('/print_list')
      
      if type == 'All':
         matlist = MatList.objects.filter(customer = cust).exclude(type = 'Labour')
         itemtype = ItemType.objects.all()
      else:
         matlist = MatList.objects.filter(customer = cust, type = type).exclude(type = 'Labour')
         itemtype = 0
      data = {
         'matlist' : matlist,
         'itemtype': itemtype,
         'cust': cust,
         'type': type
      }
      return render(request, "print_list.html", data)
   
def new_list(request):
   if request.method == 'POST':
     customers = Customer.objects.all()
     itemtypes = ItemType.objects.all()
     data = {
         'customers': customers,
         'itemtypes': itemtypes
        }  
     return render(request, "print_list.html", data)


def render_to_pdf(template_src, context_dict ={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def new_pdf(request):
    if request.method == 'POST':
        price = request.POST['price']
        if price == '1':
           if request.POST['type'] == 'All':
             matlist = MatList.objects.filter(customer = request.POST['customer']).exclude(price = 0).exclude(type = 'Labour')
             total = matlist.aggregate(Sum('price'))['price__sum']
             labour = MatList.objects.filter(customer = request.POST['customer'], type = 'Labour').aggregate(Sum('price'))['price__sum']
             ftotal = total + labour
             data = {
                  'cust' : request.POST['customer'],
                  'matlist' : matlist,
                  'type': request.POST['type'],
                  'price': int(price),
                  'total': total,
                  'labour': labour,
                  'ftotal': ftotal
                   }
           else:
               matlist = MatList.objects.filter(customer = request.POST['customer'], type = request.POST['type']).exclude(price = 0).exclude(type = 'Labour')
               total = matlist.aggregate(Sum('price'))['price__sum']
               labour = MatList.objects.filter(customer = request.POST['customer'], type = 'Labour').aggregate(Sum('price'))['price__sum']
               ftotal = total + labour
               data = {
                   'cust' : request.POST['customer'],
                   'type': request.POST['type'],
                   'matlist' : matlist,
                   'price': int(price),
                   'total': total,
                   'labour': labour,
                   'ftotal': ftotal
                   }
        else:
            if request.POST['type'] == 'All':
               matlist = MatList.objects.filter(customer = request.POST['customer']).exclude(type = 'Labour')
               data = {
               'cust' : request.POST['customer'],
               'matlist' : matlist,
               'type': request.POST['type'],
               }
            else:
               matlist = MatList.objects.filter(customer = request.POST['customer'], type = request.POST['type']).exclude(type = 'Labour')
               data = {
               'cust' : request.POST['customer'],
               'type': request.POST['type'],
               'matlist' : matlist,
               }
        pdf = render_to_pdf('pdf_list.html',data)
        filename = 'matlist_%s' %request.POST['customer']
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf'%filename 
        return response
        #return FileResponse(pdf,content_type = 'application/pdf')


def se_billing(request):
    if request.method == 'GET':
       employees = Employee.objects.all()
       data = {
          'employees': employees
       }
       return render(request, "se_billing.html", data)   
    elif request.method == 'POST':
       name = request.POST['name']
       month = request.POST['month']
       year = request.POST['year']
       if name == 'Select Employee':
          messages.error(request,"Select Employee")
          return redirect('/se_billing')
       if month == 'Select month':
          messages.error(request,"Select month")
          return redirect('/se_billing')
       if year == 'Select Year':
          messages.error(request,"Select Year")   
          return redirect('/se_billing')
       log = Etransaction.objects.filter(month = month, year  = year, employee = name)
       total_paid = Etransaction.objects.filter(month = month, year  = year, employee = name).aggregate(Sum('pay'))['pay__sum']
       data = {
          'employee': name,
          'month' : month,
          'year' : year,
          'log' : log,
          'total_paid' : total_paid
       }
       return render(request, "se_billing.html", data)


def manage_brand(request):
    if request.method=='GET':
       brand = Brand.objects.all()
    data = {
          'brands': brand
    }
    return render(request, "manage_brand.html",data)

def add_brand(request):
    if request.method=='POST':
       name = request.POST['name']
       myquery = Brand(name = name)
       myquery.save()
       messages.success(request,"Brand Added Successfully")
       return redirect('/manage_brand') 
    return render(request, "manage_brand.html")

def delete_brand(request):
    if request.method=='POST':
      id = request.POST['id']
      myquery = Brand.objects.get(id=id)
      todelete = Item.objects.filter(brand=myquery.name)
      todelete.delete()
      myquery.delete()
      messages.success(request,"Brand & Its Items Deleted Successfully")
      return redirect('/manage_brand')
    return render(request, "manage_brand.html")


def ctransaction(request):
    if request.method == 'GET':
       customers = Customer.objects.all()
       data = {
          'customers': customers
       }
       return render(request, "ctransaction.html", data)   
    elif request.method == 'POST':
       name = request.POST['name']
       month = request.POST['month']
       year = request.POST['year']
       if name == 'Select Customer':
          messages.error(request,"Select Customer")
          return redirect('/ctransaction')
       if month == 'Select month':
          messages.error(request,"Select month")
          return redirect('/ctransaction')
       if year == 'Select Year':
          messages.error(request,"Select Year")   
          return redirect('/ctransaction')
       log = Ctransaction.objects.filter(month = month, year  = year, customer = name)
       total_paid = log.aggregate(Sum('pay'))['pay__sum']
       data = {
          'customer': name,
          'month' : month,
          'year' : year,
          'log' : log,
          'total_paid' : total_paid
       }
       return render(request, "ctransaction.html", data)

      
from django.urls import path       # Every urls.py need to have this import 
from . import views                #Import view is also necessary. This can also be from electricapp import views

# Enter url path below

urlpatterns = [
    path('home',views.index, name = "index"),
    path('attendance',views.attendance, name = "attendance"),
    path('mat_list',views.mat_list, name = "mat_list"),
    path('print_list',views.print_list, name = "print_list"),
    path('new_list',views.new_list, name = "new_list"),
    path('get_list',views.get_list, name = "get_list"),
    path('c_billing',views.c_billing, name = "c_billing"),
    path('e_billing',views.e_billing, name = "e_billing"),
    path('local_admin',views.local_admin, name = "local_admin"),
    path('add_employee',views.add_employee, name = "add_employee"),
    path('update_employee',views.update_employee, name = "update_employee"),
    path('delete_employee',views.delete_employee, name = "delete_employee"),
    path('add_item',views.add_item, name = "add_item"),
    path('manage_items',views.manage_items, name = "manage_items"),
    path('manage_employees',views.manage_employees, name = "manage_employees"),
    path('manage_customers',views.manage_customers, name = "manage_customers"),
    path('manage_itemtype',views.manage_itemtype, name = "manage_itemtype"),
    path('add_itemtype',views.add_itemtype, name = "add_itemtype"),
    path('delete_itemtype',views.delete_itemtype, name = "delete_itemtype"),
    path('att_report',views.att_report, name = "att_report"),
    path('add_customer',views.add_customer, name = "add_customer"),
    path('update_customer',views.update_customer, name = "update_customer"),
    path('delete_customer',views.delete_customer, name = "delete_customer"),
    path('add_customer',views.add_customer, name = "add_customer"),
    path('update_item',views.update_item, name = "update_item"),
    path('delete_item',views.delete_item, name = "delete_item"),
    path('add_material',views.add_material, name = "add_material"),
    path('delete_material',views.delete_material, name = "delete_material"),
    path('new_material',views.new_material, name = "new_material"),
    path('new_pdf',views.new_pdf, name = "new_pdf"),
    path('se_billing',views.se_billing, name = "se_billing"),
    path('manage_brand',views.manage_brand, name = "manage_brand"),
    path('add_brand',views.add_brand, name = "add_brand"),
    path('delete_brand',views.delete_brand, name = "delete_brand"),
    path('ctransaction',views.ctransaction, name = "ctransaction"),
    
]

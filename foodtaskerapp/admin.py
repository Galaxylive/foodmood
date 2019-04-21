from django.contrib import admin

# Register your models here.
from foodtaskerapp.models import Restaurent,Customer,Driver,Meals,Order,OrderDetails
admin.site.register(Restaurent)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Meals)
admin.site.register(Order)
admin.site.register(OrderDetails)

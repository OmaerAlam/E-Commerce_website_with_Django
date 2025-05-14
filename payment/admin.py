from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

#Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend ourr Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["dateOrdered"]
    fields = ["user", "fullName", "email", "shippingAddress", "amountPaid", "dateOrdered", "shipped", "dateShipped"]
    inlines = [OrderItemInline]

#Unregister Order Model
admin.site.unregister(Order)

#Re-Register our Order and OrderItems
admin.site.register(Order, OrderAdmin)
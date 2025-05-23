from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shippingFullName= models.CharField(max_length=255)
    shippingEmail = models.CharField(max_length=255)
    shippingAddress1 = models.CharField(max_length=255)
    shippingAddress2 = models.CharField(max_length=255, null=True, blank=True)
    shippingCity = models.CharField(max_length=255)
    shippingState = models.CharField(max_length=255, null=True, blank=True)
    shippningZipcode = models.CharField(max_length=255)
    shippingCountry = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
#Create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        userShipping = ShippingAddress(user=instance)
        userShipping.save()
#Automate the profile thing
post_save.connect(create_shipping, sender=User)
    
#Create Order Model
class Order(models.Model):
    #Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    fullName = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    shippingAddress = models.TextField(max_length=15000)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2)
    dateOrdered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    dateShipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'

#Auto add shipping date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.dateShipped = now

    
#Create Order Items Model
class OrderItem(models.Model):
    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'


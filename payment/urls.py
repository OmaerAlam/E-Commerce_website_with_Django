from django.urls import path
from . import views

urlpatterns = [
    path('paymentSuccess', views.paymentSuccess, name='paymentSuccess'),
    path('checkout', views.checkout, name='checkout'),
    path('billingInfo', views.billingInfo, name='billingInfo'),
    path('processOrder', views.processOrder, name='processOrder'),
    path('shippedDash', views.shippedDash, name='shippedDash'),
    path('notshippedDash', views.notshippedDash, name='notshippedDash'),
    path('orders/<int:pk>', views.orders, name='orders'),
]

from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime

def  orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #Get the Order
        order = Order.objects.get(id=pk)

        #Get the order item
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shippingStatus']
            #Check if true or false
            if status == "true":
                #Get the order
                order = Order.objects.filter(id=pk)
                #Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, dateShipped = now)
                messages.success(request, "Order marked as shipped.")
            else:
                #Get the order
                order = Order.objects.filter(id=pk)
                #Update the status
                order.update(shipped=False)

            messages.success(request, "Order marked as not shipped.")
            return redirect('home')

        return render(request, 'payment/orders.html',{"order":order, "items":items})
    else:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')

def notshippedDash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False) 
        if request.POST:
            status = request.POST['shippingStatus']
            num = request.POST['num']
            
            #Grab the order
            order = Order.objects.filter(id=num)
            #Update date and time
            now = datetime.datetime.now()
            #Update Order 
            order.update(shipped=True, dateShipped = now) 
            #Update redirect
            messages.success(request, f"Order #{num} marked as shipped.")
            return redirect('home')
        
        return render(request, "payment/notshippedDash.html", {"orders":orders})
    else:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home') 

def shippedDash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shippingStatus']
            num = request.POST['num']

            #Grab the order
            order = Order.objects.filter(id=num)
            #Update date and time
            now = datetime.datetime.now()
            #Update Order 
            order.update(shipped=False) 
            #Update redirect
            messages.success(request, f"Order #{num} marked as not shipped.")
            return redirect('home')
        return render(request, "payment/shippedDash.html", {"orders":orders})
    else:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home') 
    
def processOrder(request):
    if request.POST:
        #Get the cart
        cart = Cart(request)
        cartProducts = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)

        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        #Gather Order Info
        fullName = my_shipping['shippingFullName']
        email = my_shipping['shippingEmail']
        #Create Shipping Address from session Info
        shippingAddress = f"{my_shipping['shippingAddress1']}\n{my_shipping['shippingAddress2']}\n{my_shipping['shippingCity']}\n{my_shipping['shippingState']}\n{my_shipping['shippningZipcode']}\n{my_shipping['shippingCountry']}\n"
        amountPaid = totals

        #Create an Order
        if request.user.is_authenticated:
            #Logged In
            user = request.user
            #Create Order
            createOrder = Order(user=user, fullName=fullName, email=email, shippingAddress=shippingAddress, amountPaid=amountPaid)
            createOrder.save()

            #add order items
            #Get the order ID
            orderId = createOrder.pk
            #Get the product ID
            for product in cartProducts():
                #Get product ID
                productId = product.id
                #Get product price
                if product.isSale:
                    price = product.salePrice
                else:
                    price = product.price

                #Get Quantity
                for key,value in quantities().items():
                    if (key) == product.id:
                        #Create Order item
                        createOrderItem = OrderItem(orderId=orderId, productId=productId, user=user, quantity=value, price=price )
                        createOrderItem.save()

            #Delete our card
            for key in list(request.session.keys()):
                if key == "sessionKey":
                    #Delete the key
                    del request.session[key]
            #Delete Cart from Database
            currentUser = Profile.objects.filter(user__id=request.user.id)
            #Delete Shopping Cart from Database
            currentUser.update(old_cart="")


            messages.success(request, "Your order has been placed successfully!")
            return redirect('home')
        else:
            #Not Logged In
            #Create Order
            createOrder = Order(fullName=fullName, email=email, shippingAddress=shippingAddress, amountPaid=amountPaid)
            createOrder.save()

            #add order items
            #Get the order ID
            orderId = createOrder.pk
            #Get the product ID
            for product in cartProducts():
                #Get product ID
                productId = product.id
                #Get product price
                if product.isSale:
                    price = product.salePrice
                else:
                    price = product.price

                #Get Quantity
                for key,value in quantities().items():
                    if (key) == product.id:
                        #Create Order item
                        createOrderItem = OrderItem(orderId=orderId, productId=productId, quantity=value, price=price)
                        createOrderItem.save()

            #Delete our card
            for key in list(request.session.keys()):
                if key == "sessionKey":
                    #Delete the key
                    del request.session[key]

            messages.success(request, "Guest order placed successfully!")
            return redirect('home')
    else:
        messages.error(request, "Invalid request. Access denied.")
        return redirect('home')  

def billingInfo(request):
    if request.POST:
        #Get the cart
        cart = Cart(request)
        cartProducts = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #Create a Session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #Check to see if user is logged In
        if request.user.is_authenticated:
            #Get the Billing Form
            billing_form = PaymentForm
            messages.success(request, "Please fill in your billing information to proceed.")
            return render(request, "payment/billingInfo.html", {"cartProducts":cartProducts, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            #Not Logged In
            #Get the Billing Form
            billing_form = PaymentForm
            return render(request, "payment/billingInfo.html", {"cartProducts":cartProducts, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "payment/billingInfo.html", {"cartProducts":cartProducts, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        messages.error(request, "You must complete shipping info first.")
        return redirect('home')

def checkout(request):
    #Get the cart
    cart = Cart(request)
    cartProducts = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #Checkout as Logged In User
        #Shipping User
        shippingUser = ShippingAddress.objects.get(user__id=request.user.id)
        #Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shippingUser)
        return render(request, "payment/checkout.html", {"cartProducts":cartProducts, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})    
    else:
        #Checkout as Guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cartProducts":cartProducts, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

def paymentSuccess(request):
    messages.success(request, "Payment was successful! Thank you for your purchase.")
    return render(request, "payment/paymentSuccess.html", {})

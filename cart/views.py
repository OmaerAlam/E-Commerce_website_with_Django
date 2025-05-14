from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cartSummery(request):
    #Get the cart
    cart = Cart(request)
    cartProducts = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cartSummery.html", {"cartProducts":cartProducts, "quantities":quantities, "totals":totals})

def cartAdd(request):
    # Get the Cart
    cart = Cart(request)
    #Test for POST
    if request.POST.get('action') == 'post':
        #Get stuff
        productId = int(request.POST.get('productId'))
        productQty = int(request.POST.get('productQty'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=productId)
        
        # Save to session
        cart.add(product=product, quantity=productQty)
        
        # Get Cart Quantity
        cartQuantity = cart.__len__()

        response = JsonResponse({'qty': cartQuantity})
        messages.success(request, f"Successfully added {product.name} to your cart!")
        return response

def cartDelete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        productId = int(request.POST.get('productId'))

        #Call delete Funtion in Cart
        product = get_object_or_404(Product, id=productId)
        cart.delete(product=productId)

        response = JsonResponse({'product':productId})
        #return redirect('cart_summary')
        messages.success(request, f"{product.name} has been removed from your cart.")
        return response
       

def cartUpdate(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
            # Get stuff
            productId = int(request.POST.get('productId'))
            productQty = int(request.POST.get('productQty'))

            # Lookup product in DB
            product = get_object_or_404(Product, id=productId)

            # Update the cart
            cart.update(product=productId, quantity=productQty)

            # Get the product name
            product_name = product.name

            response = JsonResponse({'qty': productQty})
            messages.success(request, f"Your cart has been updated. {productQty} {product_name}(s) now in the cart.")
            return response




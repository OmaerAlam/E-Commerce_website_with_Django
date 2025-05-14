from .cart import Cart

#Create context processors so our cart can work on all pages
def cart(request):
    #Return the default data from out cart
    return {'cart': Cart(request)}
from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('sessionKey')

        #If the user is new, no session key ! creat one !
        if 'sessionKey' not in request.session:
            cart = self.session['sessionKey'] = {}
        
        #Make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        productId = str(product)
        productQty = str(quantity)

        #Logic
        if productId in self.cart:
            pass
        else:
            self.cart[productId] = int(productQty)

        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2",4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            currentUser.update(old_cart=str(carty))   

    def add(self, product, quantity):
        productId = str(product.id)
        productQty = str(quantity)

        #Logic
        if productId in self.cart:
            pass
        else:
            self.cart[productId] = int(productQty)

        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2",4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            currentUser.update(old_cart=str(carty))

    def cart_total(self):
        #Get product IDS
        productsIds = self.cart.keys()
        products = Product.objects.filter(id__in=productsIds)
        #Get quantities
        quantities = self.cart
        
        #start counting at 0
        total=0
        for key, value in quantities.items():
            #Convert key string
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.isSale:
                        total = total + (product.salePrice * value)
                    else:
                        total = total + (product.price * value)
        return total

    
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get ids from cart
        productIds = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=productIds)
        # Return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        productId = str(product)
        productQty = int(quantity)

        #Get Cart
        ourcart = self.cart

        #Update Dictionary/cart
        ourcart[productId] = productQty

        self.session.modified = True
        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2",4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            currentUser.update(old_cart=str(carty))
        thing = self.cart
        return thing
    
    def delete(self, product):
        productId = str(product)
        #Delete from dictionary/cart
        if productId in self.cart:
            del self.cart[productId]

        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2",4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            currentUser.update(old_cart=str(carty))
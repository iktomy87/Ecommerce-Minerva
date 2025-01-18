from django.shortcuts import render, redirect, HttpResponseRedirect 
from .models import Producto, Categoria, Cliente, Orden
from django.views import View 
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Index(View):
    def post(self, request):
        product_id = request.POST.get('producto')  
        remove = request.POST.get('remove') 
        cart = request.session.get('cart', {}) 

    
        request.session['cart'] = update_cart(cart, product_id, remove=bool(remove))

        print('Carrito actualizado:', request.session['cart'])  

        return redirect('homepage')  

    def get(self, request):
        return redirect('homepage')  

  
def store(request): 
    cart = request.session.get('cart') 
    if not cart: 
        request.session['cart'] = {} 
    productos = None
    categorias = Categoria.get_all_categorias() 
    categoryID = request.GET.get('categoria') 
    if categoryID: 
        productos = Producto.get_all_products_by_categoryid(categoryID) 
    else: 
        productos = Producto.get_all_products() 
  
    data = {} 
    data['productos'] = productos
    data['categorias'] = categorias
  
    print('you are : ', request.session.get('email')) 
    return render(request, 'index.html', data) 


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        if request.session.get('customer'):
            return redirect('homepage') 
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Cliente.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage') 
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})
  
  
def logout(request): 
    request.session.clear() 
    return redirect('login') 


class Signup (View): 
    def get(self, request): 
        return render(request, 'signup.html') 
  
    def post(self, request): 
        postData = request.POST 
        first_name = postData.get('firstname') 
        last_name = postData.get('lastname') 
        phone = postData.get('phone') 
        email = postData.get('email') 
        password = postData.get('password') 
        # validation 
        value = { 
            'first_name': first_name, 
            'last_name': last_name, 
            'phone': phone, 
            'email': email 
        } 
        error_message = None
  
        customer = Cliente(first_name=first_name, 
                            last_name=last_name, 
                            phone=phone, 
                            email=email, 
                            password=password) 
        error_message = self.validateCustomer(customer) 
  
        if not error_message: 
            print(first_name, last_name, phone, email, password) 
            customer.password = make_password(customer.password) 
            customer.register() 
            return redirect('homepage') 
        else: 
            data = { 
                'error': error_message, 
                'values': value 
            } 
            return render(request, 'signup.html', data) 
  
    def validateCustomer(self, customer): 
        error_message = None
        if not customer.first_name: 
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3: 
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name: 
            error_message = 'Please Enter your Last Name'
        elif len(customer.last_name) < 3: 
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone: 
            error_message = 'Enter your Phone Number'
        elif len(customer.phone) != 10 or not customer.phone.isdigit(): 
            error_message = 'Phone Number must be 10 digits long'
        elif len(customer.password) < 5: 
            error_message = 'Password must be 5 char long'
        elif len(customer.email) < 5: 
            error_message = 'Email must be 5 char long'
        else:
            try:
                validate_email(customer.email)
            except ValidationError:
                error_message = 'Invalid Email Address'

        if customer.isExists(): 
            error_message = 'Email Address Already Registered..'
        
        return error_message
    
class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        if not customer:
            return redirect('login') 
        cart = request.session.get('cart')
        products = Producto.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Orden(cliente=Cliente(id=customer),
                          producto=product,
                          precio=product.precio,
                          direccion=address,
                          telefono=phone,
                          cantidad=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        product.stock -= cart.get(str(product.id))
        product.save()

        return redirect('cart')
    

@method_decorator(login_required, name='dispatch')
class OrderView(View): 
    def get(self, request): 
        customer = request.session.get('customer') 
        orders = Orden.get_orders_by_customer(customer) 
        return render(request, 'orders.html', {'orders': orders})
    

def update_cart(cart, product, remove=False):
    quantity = cart.get(product, 0)
    if remove:
        if quantity <= 1:
            cart.pop(product)
        else:
            cart[product] -= 1
    else:
        cart[product] += 1

class CartView(View):
    def get(self, request):

        if not request.session.get('customer'):
            return redirect('login') 

        cart = request.session.get('cart', {})
        products = Producto.get_products_by_id(list(cart.keys()))
        
        return render(request, 'cart.html', {'cart': cart, 'products': products})
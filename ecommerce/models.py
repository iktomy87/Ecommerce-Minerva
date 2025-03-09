# store/models.py
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings

class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categorias"

    @staticmethod
    def get_all_categorias(): 
        return Categoria.objects.all() 
  
    def __str__(self): 
        return self.nombre 

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField( 
        max_length=250, default='', blank=True, null=True) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)

    @staticmethod
    def get_products_by_id(ids): 
        return Producto.objects.filter(id__in=ids) 
  
    @staticmethod
    def get_all_products(): 
        return Producto.objects.all() 
  
    @staticmethod
    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        try:
            return Producto.objects.filter(categoria=category_id) 
        except Categoria.DoesNotExist:
            return Producto.get_all_products()
        
    def reduce_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
        else:
            raise ValueError("Stock insuficiente")

    
class Cliente(models.Model): 
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    phone = models.CharField(max_length=10) 
    email = models.EmailField() 
    password = models.CharField(max_length=100) 
  
    def register(self): 
        self.save() 
  
    @staticmethod
    def get_customer_by_email(email): 
        try: 
            return Cliente.objects.get(email=email) 
        except: 
            return False
  
    def isExists(self): 
        if Cliente.objects.filter(email=self.email): 
            return True
  
        return False

class Orden(models.Model): 
    producto = models.ForeignKey(Producto, 
                                on_delete=models.CASCADE) 
    cliente = models.ForeignKey(Cliente, 
                                 on_delete=models.CASCADE) 
    cantidad = models.IntegerField(default=1) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=50, default='', blank=True) 
    telefono = models.CharField(max_length=50, default='', blank=True) 
    fecha = models.DateField(default=datetime.datetime.today) 
    estado = models.BooleanField(default=False) 
  
    def placeOrder(self): 
        self.save() 
  
    @staticmethod
    def get_orders_by_customer(customer_id): 
        return Orden.objects.filter(cliente=customer_id).order_by('-fecha') 




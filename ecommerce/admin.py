from django.contrib import admin
from .models import Producto, Cliente, Categoria, Orden


admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Orden)
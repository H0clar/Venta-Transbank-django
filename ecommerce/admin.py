from django.contrib import admin
from .models import Cliente, Producto, CarritoDeCompras, Item, Boleta

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class BoletaAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'correo')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'img')

class CarritoDeComprasAdmin(admin.ModelAdmin):
    list_display = ('id', 'total')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'boleta', 'producto', 'cantidad', 'subtotal')  # Agregamos 'boleta' a la lista de display

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(CarritoDeCompras, CarritoDeComprasAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Boleta, BoletaAdmin)

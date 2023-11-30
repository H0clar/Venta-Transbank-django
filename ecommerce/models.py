from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Boleta(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    total = models.IntegerField()  # Cambiado de Decimal a Integer

    def __str__(self):
        return f"Boleta {self.id} - Cliente: {self.cliente.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.IntegerField()  # Cambiado de Decimal a Integer
    img = models.URLField(blank=True)

    def __str__(self):
        return self.nombre

class CarritoDeCompras(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    total = models.IntegerField(default=0)  # Cambiado de Decimal a Integer

    def __str__(self):
        return f"Carrito de {self.cliente.nombre if self.cliente else 'Usuario Anónimo'}"

class Item(models.Model):
    carrito = models.ForeignKey(CarritoDeCompras, related_name='items', on_delete=models.CASCADE)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.IntegerField()  # Cambiado de Decimal a Integer

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

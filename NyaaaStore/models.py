from django.db import models
from .enumeraciones import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# MODELO ANIME
class Anime(models.Model):
    nombre=models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.nombre

# MODELO MARCA    
class Marca(models.Model):
    nombre=models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.nombre

# MODELO SERIE
class Serie(models.Model):
    nombre=models.CharField(max_length=500, null=False)
    marca=models.ForeignKey(Marca, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

# MODELO PRODUCTO
class Producto(models.Model):
    nombre=models.CharField(max_length=1000, null=False)
    anime=models.ForeignKey(Anime, on_delete=models.PROTECT)
    marca=models.ForeignKey(Marca, on_delete=models.PROTECT)
    serie=models.ForeignKey(Serie, on_delete=models.PROTECT)
    descripcion=models.TextField(max_length=5000, null=False)
    tp_producto=models.CharField(max_length=15, choices=TIPO_PRODUCTO, default='SIN ESPECIFICAR')
    precio=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(400000)])
    stock=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    foto=models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre

# MODELO PERFIL
class UserPerfil(models.Model):
    usuario=models.OneToOneField(User, related_name='usuario', on_delete=models.CASCADE)
    fono=models.CharField(max_length=9, null=False)
    city=models.CharField(max_length=15, choices=CIUDAD, null=False)
    direccion=models.CharField(max_length=200, null=False)

# MODELO CARRITO 

class CartItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_por_item = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def subtotal(self):
        return self.cantidad * self.precio_por_item

    def __str__(self):
        return f"{self.juego} - {self.cantidad} x {self.precio_por_item}"

class Cart(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario", related_name="carts")
    items = models.ManyToManyField(CartItem, verbose_name="Ítems", related_name="carts")

    def total(self):
        return sum([item.subtotal() for item in self.items.all()])

    def __str__(self):
        return f"Cart for {self.usuario}"

# Ventas
class Venta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField()
    total_venta = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADO, default='EN PREPARACIÓN')

    def total_venta(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"Venta {self.id} - {self.producto.nombre} - {self.cantidad} unidades"
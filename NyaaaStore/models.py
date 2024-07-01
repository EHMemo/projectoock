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
from django.contrib import admin
from .models import Anime,Marca,Serie,Producto,Venta

# En la tabla de la DB muestra por categoria los datos
class AdmMarca(admin.ModelAdmin):
    list_display=['id','nombre']

    # filtra en la tabla de la DB
    list_filter=['nombre']

class AdmSerie (admin.ModelAdmin):
    list_display=['id','nombre','marca']

    # filtra en la tabla de la DB
    list_filter=['nombre','marca']

class AdmAnime (admin.ModelAdmin):
    list_display=['id','nombre']

    # filtra en la tabla de la DB
    list_filter=['nombre']

class AdmProducto (admin.ModelAdmin):
    list_display=['foto','id','nombre','anime','marca','serie','descripcion','tp_producto','precio','stock']

    # filtra en la tabla de la DB
    list_filter=['anime','marca','serie']
# Register your models here.
admin.site.register(Marca,AdmMarca)
admin.site.register(Serie,AdmSerie)
admin.site.register(Anime,AdmAnime)
admin.site.register(Producto,AdmProducto)
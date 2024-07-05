from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from os import remove, path
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import random


# Create your views here.

# VIEWS PAGINA BASE

def home(request):
    productos = list(Producto.objects.all())
    random.shuffle(productos)
    return render(request, 'NyaaaStore/home.html', {'productos': productos})

def cat_figuras(request):
    
    productos = Producto.objects.filter(tp_producto='FIGURA')
    datos = {
        'productos': productos
    }

    return render(request, 'NyaaaStore/catalogo_figuras.html', datos)

def cat_poleras(request):

    productos = Producto.objects.filter(tp_producto='POLERA')
    datos = {
        'productos': productos
    }

    return render(request, 'NyaaaStore/catalogo_poleras.html', datos)

def cat_accesorios(request):

    productos = Producto.objects.filter(tp_producto='ACCESORIO')
    datos = {
        'productos': productos
    }

    return render(request, 'NyaaaStore/catalogo_accesorios.html', datos)

def register(request):

    data={
        'form':UserForm()
    }

    if request.method=='POST':
        formulario=UserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user=authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Logeo exitoso")
            #redirige al index
            return redirect(to='home')
        data["form"]=formulario
    return render(request, 'registration/register.html', data)

def verproducto(request, id):
    producto=get_object_or_404(Producto, id=id)
    
    datos={
        "producto":producto
    }

    return render(request,'NyaaaStore/detalleproducto.html', datos)

def exit(request):
    logout(request)
    
    return redirect('home')

@login_required
def carrito(request):
    cart, created = Cart.objects.get_or_create(usuario=request.user)
    return render(request, 'NyaaaStore/cart.html', {'cart': cart})

@login_required
def perfil(request, username):

    usuario=get_object_or_404(User, username=username)
    historial_compras = Venta.objects.filter(usuario=usuario).order_by('-fecha')
    perfil_usuario = get_object_or_404(UserPerfil, usuario=usuario)

    datos={
        'usuario':usuario,
        'historial_compras': historial_compras,
        'perfil_usuario': perfil_usuario,
    }

    return render(request, 'NyaaaStore/perfil.html', datos)

@login_required
def editar_perfil(request):

    if request.method == 'POST':
        form = UptadeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect(reverse('perfil', args=[request.user.username]))
    else:
        form = UptadeUserForm(instance=request.user)

    return render(request, 'NyaaaStore/editarperfil.html', {'form': form})

@login_required
def editar_contacto(request):

    usuario_profile, created = UserPerfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=usuario_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos de contacto han sido actualizados exitosamente.')
            return redirect(reverse('perfil', args=[request.user.username]))
    else:
        form = ContactoForm(instance=usuario_profile)

    return render(request, 'NyaaaStore/contacto.html', {'form': form})

# FUNCIONES CARRITO

@login_required
def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart, created = Cart.objects.get_or_create(usuario=request.user)

    cart_item, created = CartItem.objects.get_or_create(producto=producto, precio_por_item=producto.precio)
    if not created:
        cart_item.cantidad += 1
        cart_item.save()

    cart.items.add(cart_item)
    messages.success(request, f'{producto.nombre} fue añadido a tu carrito.')

    return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        cart_item.cantidad = cantidad
        cart_item.save()
        messages.success(request, 'La cantidad fue actualizada.')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'El ítem fue eliminado del carrito.')
    return redirect('cart')

@login_required
def process_payment(request):
    cart, created = Cart.objects.get_or_create(usuario=request.user)
    if not cart.items.exists():
        messages.error(request, 'No tienes artículos en tu carrito.')
        return redirect('cart')

    for item in cart.items.all():
        producto = item.producto
        if item.cantidad > producto.stock:
            messages.error(request, f'No hay suficiente stock para {producto.nombre}.')
            return redirect('cart')
        
        Venta.objects.create(
                usuario=request.user,
                producto=producto,
                cantidad=item.cantidad,
                estado='EN PREPARACIÓN',
                fecha=timezone.now()
            )
        
    for item in cart.items.all():
        producto = item.producto
        producto.stock -= item.cantidad
        producto.save()

    cart.items.clear()
    
    messages.success(request, 'Pago realizado con éxito. Gracias por tu compra.')
    return redirect('cart')

# FIN FUNCIONES CARRITO
# FIN VIEWS PAGINA BASE

# VIEWS VISTA ADMIN
@permission_required('NyaaaStore.view_anime')
@permission_required('NyaaaStore.add_anime')
@permission_required('NyaaaStore.view_marca')
@permission_required('NyaaaStore.add_marca')
@permission_required('NyaaaStore.view_anime')
@permission_required('NyaaaStore.add_anime')
@permission_required('NyaaaStore.add_producto')
@permission_required('NyaaaStore.view_producto')
@permission_required('NyaaaStore.change_producto')
@permission_required('NyaaaStore.delete_producto')
@permission_required('NyaaaStore.view_user')
@permission_required('NyaaaStore.change_user')
@permission_required('NyaaaStore.delete_user')
@permission_required('NyaaaStore.add_user')
@login_required
def home_adm(request):

    return render(request, 'NyaaaStore/vistaadm/home-adm.html')

@permission_required('NyaaaStore.view_venta')
@login_required
def ventas(request):

    ventas = Venta.objects.all().order_by('-fecha')

    if request.method == 'POST':
        venta_id = request.POST.get('venta_id')
        venta = get_object_or_404(Venta, id=venta_id)
        form = EstadoVentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('vistaVentas')
    else:
        form = EstadoVentaForm()

    datos={
        'ventas': ventas,
        'form': form
    }

    return render(request, 'NyaaaStore/Ventas.html', datos)

# FORMULARIO ANIME

@permission_required('NyaaaStore.view_anime')
def listar_anime(request):

    anime=Anime.objects.all()
    page=request.GET.get('page',1)

    try:
        paginator=Paginator(anime, 5)
        anime=paginator.page(page)
    except:
        raise Http404
    
    datos={
        'entity':anime,
        'paginator':paginator
    }
    
    return render(request, 'NyaaaStore/anime/listar.html', datos)

@permission_required('NyaaaStore.add_anime')
def agregar_anime(request):

    datos={
        'formanime':AnimeForm()
    }

    if request.method=="POST":
        formulario=AnimeForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Anime agregado")
            return redirect(to="listar_anime")
        else:
            datos["formanime"]=formulario

    return render(request, 'NyaaaStore/anime/agregar.html', datos)

@permission_required('NyaaaStore.delete_anime')
def eliminar_anime(request, id=id):
    anime = get_object_or_404(Anime, id=id)
    anime.delete()
    return redirect(to=listar_anime)

# FIN FORMULARIO ANIME

# FORMULARIO MARCA

@permission_required('NyaaaStore.view_marca')
def listar_marca(request):

    marca=Marca.objects.all()
    page=request.GET.get('page',1)

    try:
        paginator=Paginator(marca, 5)
        marca=paginator.page(page)
    except:
        raise Http404
    
    datos={
        'entity':marca,
        'paginator':paginator
    }
    
    return render(request, 'NyaaaStore/marca/listar.html', datos)

@permission_required('NyaaaStore.add_marca')
def agregar_marca(request):

    datos={
        'form':MarcaForm()
    }

    if request.method=="POST":
        formulario=MarcaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Marca agregado")
            return redirect(to="listar_marca")
        else:
            datos["form"]=formulario

    return render(request, 'NyaaaStore/marca/agregar.html', datos)

@permission_required('NyaaaStore.delete_marca')
def eliminar_marca(request, id=id):
    marca = get_object_or_404(Marca, id=id)
    marca.delete()
    messages.warning(request, "Marca eliminada")
    return redirect(to=listar_marca)

# FIN FORMULARIO MARCA

# FORMULARIO SERIE

@permission_required('NyaaaStore.view_serie')
def listar_serie(request):

    serie=Serie.objects.all()
    page=request.GET.get('page',1)

    try:
        paginator=Paginator(serie, 5)
        serie=paginator.page(page)
    except:
        raise Http404
    
    datos={
        'entity':serie,
        'paginator':paginator
    }

    return render(request, 'NyaaaStore/serie/listar.html', datos)

@permission_required('NyaaaStore.add_serie')
def agregar_serie(request):

    datos={
        'form':SerieForm()
    }

    if request.method=="POST":
        formulario=SerieForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Serie agregado")
            return redirect(to="listar_serie")
        else:
            datos["form"]=formulario

    return render(request, 'NyaaaStore/serie/agregar.html', datos)

@permission_required('NyaaaStore.delete_serie')
def eliminar_serie(request, id=id):
    serie = get_object_or_404(Serie, id=id)
    serie.delete()
    
    return redirect(to=listar_serie)

# FIN FORMULARIO SERIE

# FIN VISTA ADMIN

# VIEWS CRUD PRODUCTOS DESDE ADMIN

@permission_required('NyaaaStore.add_producto')
def agregar_producto(request):

    datos={
        'form':ProductoForm()
    }

    if request.method == "POST":
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto agregado")
            return redirect(to="listar_producto")
        else:
            datos["form"] = formulario

    return render(request, 'NyaaaStore/producto/agregar.html', datos)

@permission_required('NyaaaStore.view_producto')
def listar_productos(request):

    productos=Producto.objects.all()
    page=request.GET.get('page', 1)

    try:
        paginator=Paginator(productos, 5)
        productos=paginator.page(page)
    except:
        raise Http404

    datos={
        'entity':productos,
        'paginator':paginator
    }
    return render(request, 'NyaaaStore/producto/listar.html', datos)

@permission_required('NyaaaStore.change_producto')
def modificar_producto(request, id):

    producto=get_object_or_404(Producto, id=id)
    
    data={
        'form':UpdateProductoForm(instance=producto)
    }

    if request.method == "POST":
        formulario=UpdateProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto modificado")
            return redirect(to="listar_producto")
        data["form"]=formulario

    return render(request, 'NyaaaStore/producto/modificar.html', data)

@permission_required('NyaaaStore.view_producto')
def detalle_producto(request, id):

    producto=get_object_or_404(Producto, id=id)

    datos={
        'producto':producto
    }

    return render(request, 'NyaaaStore/producto/detalle.html', datos)

@permission_required('NyaaaStore.delete_producto')
def eliminar_producto(request,id):
    producto=get_object_or_404(Producto, id=id)
    
    if request.method=="POST":
        
        #from os import remove, path
        #from django.conf import settings
        remove(path.join(str(settings.MEDIA_ROOT).replace('/media',''))+producto.foto.url)
        producto.delete()
        return redirect(to="listar_producto")
        
    datos={
        "producto":producto
    }
    
    return render(request,'NyaaaStore/producto/eliminar.html', datos)

# FIN VIEWS CRUD PRODUCTOS DESDE ADMIN

# VIEWS CRUD USUARIOS DESDE ADMIN

@permission_required('NyaaaStore.view_user')
def listar_cliente(request):

    #usuarios = User.objects.exclude(is_superuser=True)
    usuarios = User.objects.exclude(is_superuser=True).select_related('userperfil')
    page = request.GET.get('page', 1)
    

    try:
        paginator = Paginator(usuarios, 5)
        usuarios = paginator.page(page)
    except:
        raise Http404

    datos = {
        'entity': usuarios,
        'paginator': paginator
    }
    return render(request, 'NyaaaStore/cliente/listar.html', datos)

@permission_required('NyaaaStore.add_user')
def agregar_cliente(request):

    datos={
        'form':UserForm()
    }

    if request.method == "POST":
        formulario = UserForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos["mensaje"] = "Cliente agregado"
            return redirect(to="listar_cliente")
        else:
            datos["form"] = formulario

    return render(request, 'NyaaaStore/cliente/agregar.html', datos)

@permission_required('NyaaaStore.view_user')
def detalle_cliente(request, id):

    usuario=get_object_or_404(User, id=id)

    datos={
        'usuario':usuario
    }

    return render(request, 'NyaaaStore/cliente/detalle.html', datos)

@permission_required('NyaaaStore.change_user')
def modificar_cliente(request, id):
    usuario = get_object_or_404(User, id=id)
    perfil_usuario = get_object_or_404(UserPerfil, usuario=usuario)

    if request.method == "POST":
        user_form = UptadeUserForm(request.POST, instance=usuario)
        contacto_form = ContactoForm(request.POST, instance=perfil_usuario)
        if user_form.is_valid() and contacto_form.is_valid():
            user_form.save()
            contacto_form.save()
            messages.success(request, "Cliente modificado")
            return redirect('listar_cliente')
    else:
        user_form = UptadeUserForm(instance=usuario)
        contacto_form = ContactoForm(instance=perfil_usuario)

    datos = {
        'user_form': user_form,
        'contacto_form': contacto_form
    }

    return render(request, 'NyaaaStore/cliente/modificar.html', datos)

@permission_required('NyaaaStore.delete_user')
def eliminar_cliente(request, id):

    usuario = get_object_or_404(User, id=id)

    if request.method=="POST":
        UserPerfil.objects.filter(usuario=usuario).delete()
        usuario.delete()
        messages.warning(request, "Cliente eliminado")
        return redirect(to='listar_cliente')
    
    datos={
        'usuario':usuario
    }

    return render(request, 'NyaaaStore/cliente/eliminar.html', datos)

# FIN VIEWS CRUD USUARIOS DESDE ADMIN
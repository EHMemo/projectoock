from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .cart import Cart
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from os import remove, path
from django.conf import settings

# Create your views here.

# VIEWS PAGINA BASE

def home(request):
    return render(request, 'NyaaaStore/home.html')

def cat_figuras(request):
    
    productos=Producto.objects.all() #queryset
    datos = {
        'productos' : productos
    }
    return render(request, 'NyaaaStore/catalogo_figuras.html', datos)

def cat_poleras(request):
    return render(request, 'NyaaaStore/catalogo_poleras.html')

def cat_accesorios(request):
    return render(request, 'NyaaaStore/catalogo_accesorios.html')

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

def carrito(request):
    return render(request, 'NyaaaStore/carrito.html')

@login_required
def perfil(request, id):

    usuario=get_object_or_404(User, id=id)

    datos={
        'usuario':usuario
    }

    return render(request, 'NyaaaStore/perfil.html', datos)

# FUNCIONES CARRITO



# FIN FUNCIONES CARRITO
# FIN VIEWS PAGINA BASE

# VIEWS VISTA ADMIN

def home_adm(request):

    return render(request, 'NyaaaStore/vistaadm/home-adm.html')

# FORMULARIO ANIME

@permission_required('NyaaaStore.view_anime')
def listar_anime(request):

    anime=Anime.objects.all()
    page=request.GET.get('page',1)

    try:
        paginator=Paginator(anime, 7)
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

# FIN FORMULARIO ANIME

# FORMULARIO MARCA

@permission_required('NyaaaStore.view_marca')
def listar_marca(request):

    marca=Marca.objects.all()
    page=request.GET.get('page',1)

    try:
        paginator=Paginator(marca, 7)
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

# FIN FORMULARIO MARCA

# FORMULARIO SERIE

@permission_required('NyaaaStore.view_anime')
def listar_serie(request):

    serie=Serie.objects.all()
    page=request.GET.get('page',1)

    try:
        paginator=Paginator(serie, 7)
        serie=paginator.page(page)
    except:
        raise Http404
    
    datos={
        'entity':serie,
        'paginator':paginator
    }

    return render(request, 'NyaaaStore/serie/listar.html', datos)
@permission_required('NyaaaStore.add_anime')
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
        paginator=Paginator(productos, 7)
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

    query=request.GET.get('q')

    if query:
        perfiles=UserPerfil.object.filter(
            Q(usuario__id__icontains=query) |
            Q(usuario__username__icontains=query) |
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(usuario__email__icontains=query) |
            Q(fono__id__icontains=query) |
            Q(city__id__icontains=query) |
            Q(direccion__id__icontains=query)
        )
        if not perfiles.exists():
            perfiles=UserPerfil.objects.all()
    else:
        perfiles=UserPerfil.objects.all()

    datos={
        "perfiles":perfiles
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
    perfil_usuario=get_object_or_404(UserPerfil, usuario=usuario)

    if request.method=="POST":
        form=UpdateUserPerfilForm(request.POST, isinstance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.warning(request, "Cliente modificado")
            return redirect(to='listar_cliente')
        else:
            form=UpdateUserPerfilForm(isinstance=perfil_usuario)

        datos={
            'form':form
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
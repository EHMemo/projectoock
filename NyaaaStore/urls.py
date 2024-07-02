from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home,cat_figuras,cat_poleras,cat_accesorios,\
    agregar_producto,listar_productos,modificar_producto,detalle_producto,eliminar_producto,\
    home_adm,listar_anime,agregar_anime,listar_marca,agregar_marca,listar_serie,agregar_serie,\
    register,listar_cliente,agregar_cliente,modificar_cliente,detalle_cliente,eliminar_cliente,exit,verproducto,\
    perfil,carrito,add_to_cart,update_cart_item,remove_from_cart,process_payment,editar_perfil

urlpatterns = [
    path('', home, name='home'),
    path('catalogo_figuras', cat_figuras, name='catalogo_figuras'),
    path('catalogo_poleras', cat_poleras, name='catalogo_poleras'),
    path('catalogo_accesorios', cat_accesorios, name='catalogo_accesorios'),
    path('perfil/<str:username>/', perfil, name='perfil'),
    path('editarperfil/', editar_perfil, name='editarperfil'),
    path('carrito/', carrito, name='carrito'),
    # URLS CARRITO
    path('add/<int:producto_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('process_payment/', process_payment, name='process_payment'),
    # FIN URLS FUNCIONES CARRITO
    path('verproducto/<id>', verproducto, name='verproducto'),
    # URLS VISTA ADMIN
    path('vista-amd/', home_adm, name='vista-adm'),
    # FIN URLS VISTA ADMIN
    # URLS FORMULARIO ANIME
    path('listar-anime/', listar_anime, name='listar_anime'),
    path('agregar-anime/', agregar_anime, name='agregar_anime'),
    # FIN URLS FORMULARIO ANIME
    # URLS FORMULARIO MARCA
    path('listar-marca/', listar_marca, name='listar_marca'),
    path('agregar-marca/', agregar_marca, name='agregar_marca'),
    # FIN URLS FORMULARIO MARCA
    # URLS FORMULARIO SERIE
    path('listar-serie/', listar_serie, name='listar_serie'),
    path('agregar-serie/', agregar_serie, name='agregar_serie'),
    # FIN URLS FORMULARIO SERIE
    # URLS CRUD PRODUCTO DESDE ADMIN
    path('agregar-producto/', agregar_producto, name='agregar_producto'),
    path('listar-producto/', listar_productos, name='listar_producto'),
    path('modificar-producto/<id>/', modificar_producto, name='modificar_producto'),
    path('detalle-producto/<id>/', detalle_producto, name='detalle_producto'),
    path('eliminar-producto/<id>/', eliminar_producto, name='eliminar_producto'),
    # FIN URLS CRUD PRODUCTO DESDE ADMIN
    # URLS CRUD CLIENTE DESDE ADMIN
    path('agregar-cliente/', agregar_cliente, name='agregar_cliente'),
    path('listar-cliente/', listar_cliente, name='listar_cliente'),
    path('modificar-cliente/<id>/', modificar_cliente, name='modificar_cliente'),
    path('detalle-cliente/<id>/', detalle_cliente, name='detalle_cliente'),
    path('eliminar-cliente/<id>/', eliminar_cliente, name='eliminar_cliente'),
    # FIN URLS CURD CLIENTE DESDE ADMIN
    # URLS FORMS USUARIO
    path('register/', register, name='register'),
    path('logout/', exit, name='exit'),
    # FIN URLS FORMS USUARIO
]
"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from main import views

from django.contrib.auth.views import LoginView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes', views.lista_clientes),
    path('clientes/new', views.register_request),
    path('clientes/delete/<int:id>', views.delete_user),
    path('clientes/update/<int:id>', views.perfil_update),
    path('libros', views.lista_libros_all),
    path('libros/digital', views.lista_libros_digital),
    path('libros/fisico', views.lista_libros_fisico),
    path('', views.escaparate),
    path('libro/<int:id_libro>', views.detalle_libro),
    path('descarga/<int:id>', views.descargar_pdf),

    path('libro/cat/<str:categoria_nombre>', views.filtrar_por_categoria),
    path('libro/titulo', views.filtrar_por_titulo),
    path('libro/delete/<int:id_libro>', views.delete_libro),

    path('', include('stripeAPI.urls')),
    path('incidencias/', views.incidencias),
    path('incidencias/listar', views.ver_incidencias),

    path('libro/add/', views.add_libro),
    path('libro/update/<int:id_libro>', views.update_libro),


    path('pedidos/', views.pedidos),
    path('pedido/<int:id_pedido>', views.detalle_pedido),

    path('pedidos/all', views.pedidos_all),
    path('pedido/state/<int:id>', views.pedido_update_state),


    path('perfil/', views.perfil),
    path('perfil/update/<int:id>', views.perfil_update),
    path('account/delete/<int:id>', views.delete_user),

    path('login/',  LoginView.as_view(template_name='usuario/login.html')),
    path("register/", views.register_request),
    path("logout/", views.custom_logout),
    path('cesta/', views.cesta, name="Cesta"),
    path('agregar/<int:producto_id>', views.agregar_producto, name="Add"),
    path('agregarNew/<int:producto_id>', views.agregar_nuevo_producto, name="AddNew"),
    path('agregarNewDetails/<int:producto_id>', views.agregar_producto_desde_detalles, name="AddNewDetails"),
    path('eliminar/<int:producto_id>', views.eliminar_producto, name="Del"),
    path('restar/<int:producto_id>', views.restar_producto, name="Sub"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),

    path('politica/privacidad', views.politica_privacidad),
    path('politica/envios', views.envios),
    path('politica/devolucion', views.devolucion),
    path('politica/datosempresa', views.datosempresa),
]

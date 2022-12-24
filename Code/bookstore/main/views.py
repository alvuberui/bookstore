
from main.models import Libro, elegirCategoria

from main.models import Pedido
from main.models import Libro

from main.models import LibrosPedido

import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from main.models import Incidencia

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect
from django.contrib import messages
from .forms import updateProfileForm
from main.Carrito import Carrito
from stripeAPI.views import hay_fisico_bro 
from main.models import STATE_LIST, get_categorias_choices

import re


#LIBROS
from django.shortcuts import  render, redirect
from .forms import NewUserForm, newLibro, newIncidencia
from django.contrib.auth import login,logout
from django.contrib import messages



#ADMINISTRADOR

def add_libro(request):
    if request.user.is_superuser:
        if request.POST:
            form = newLibro(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                for err in form.errors.values():
                    messages.error(request, err)
        form = newLibro()
        return render (request, 'administrador/libro_add.html', context={"new_libro_form":form})
    else:
        messages.error(request, "No dispone de permisos para añadir libros")
        return redirect('/')

@login_required
def lista_clientes(request):
    if request.user.is_superuser:
        clientes=User.objects.all()
        return render(request,'administrador/lista_clientes.html', {'clientes':clientes,'MEDIA_URL': settings.MEDIA_URL})
    else:
        messages.error(request, "No dispone de permisos de administrador")
        return redirect('/')

@login_required
def pedidos_all(request):
    if request.user.is_superuser:
        pedidos=Pedido.objects.all()
        return render(request,'pedidos/lista.html', {'pedidos':pedidos,'MEDIA_URL': settings.MEDIA_URL})
    else:
        messages.error(request, "No dispone de permisos de administrador")
        return redirect('/')


@login_required
def update_libro(request, id_libro):
    if request.user.is_superuser:

        libro = get_object_or_404(Libro, pk=id_libro)
        if request.POST:
            form = newLibro(request.POST, request.FILES, instance=libro)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                for err in form.errors.values():
                    messages.error(request, err)
        form = newLibro(instance=libro)
        return render (request, 'administrador/libro_add.html', context={"new_libro_form":form})
    else:
        messages.error(request, "No dispone de permisos para actualizar libros")
        return redirect('/')




@login_required
def pedido_update_state(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    if request.user.is_superuser:
        estado = request.GET.get('estado')
        if estado in STATE_LIST:
            pedido.estado = estado
            pedido.save()
            return redirect('/pedido/'+str(id))
        else:
            messages.error(request, "No ha introducido un estado valido")
            return redirect('/pedido/'+str(id))
    else:
        messages.error(request, "No dispone de permisos de administrador")
        return redirect('/')


def descargar_pdf(request, id):
    # Create a file-like buffer to receive PDF data.

    libro = get_object_or_404(Libro, pk=id)

    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(10, 800, libro.titulo)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename= '{}.pdf'.format(libro.titulo))




#Muestra una lista de los libros
def lista_libros_all(request):
    libros=Libro.objects.all()
    return render(request,'libros/libros.html', {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})

def lista_libros_digital(request):
    libros=Libro.objects.filter(formato="DIGITAL")
    return render(request,'libros/libros.html', {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})

def lista_libros_fisico(request):
    libros=Libro.objects.filter(formato="FISICO")
    return render(request,'libros/libros.html', {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})

def escaparate(request):
    libros=Libro.objects.filter(escaparate=True)
    return render(request, "libros/libros.html",   {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})

def detalle_libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    return render(request,'libros/libroDetalle.html', {'datoLibro':libro,'MEDIA_URL': settings.MEDIA_URL})

#Lista de pedidos de un usuario
@login_required
def pedidos(request):
    pedidos= Pedido.objects.filter(usuario_id=request.user.pk)
    return render(request,'pedidos/lista.html', {'pedidos':pedidos,'MEDIA_URL': settings.MEDIA_URL})

#detalles de un pedido

def detalle_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)
    pedidoLibro = LibrosPedido.objects.filter(pedido_id=id_pedido) #todos los libros de un pedido
    total = 0 #total del pedido
    if request.user.id == pedido.usuario_id or request.user.is_superuser:
        libros = {} #diccionario de libros

        for libro in pedidoLibro:
            precio= Libro.objects.filter(id=libro.libro_id).values('precio')
            total = total + (precio[0]['precio'])*libro.cantidad
            if total <= 20 and hay_fisico_bro(request):
                total += 5
            libros[Libro.objects.get(id=libro.libro_id)] = libro.cantidad

        return render(request,'pedidos/detalles.html', {'pedido':pedido,'libros':libros,'total':total,'MEDIA_URL': settings.MEDIA_URL, 'hay_fisico': hay_fisico_bro(request)})
    else:
        messages.error(request, "No dispone de permisos para ver este pedido")
        return redirect('/')

#INDEX
def index(request):
    return render(request, 'index.html')




    
@login_required
def perfil(request):
    return render(request, 'usuario/perfil.html')


def actualizar_perfil_form(usuario, request):
        form = updateProfileForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente")
        else:
            for err in form.errors.values():
                messages.error(request, err)

@login_required
def perfil_update(request, id):
        if request.POST:   #PARA POST
            if request.user.is_superuser and request.user.id != id:
                usuario = get_object_or_404(User, pk=id)
                actualizar_perfil_form(usuario, request)
                return redirect("/clientes")
            elif request.user.id == id:
                actualizar_perfil_form(request.user, request)
                form = updateProfileForm(instance=request.user)
                return render(request, "usuario/actualizar_perfil.html", {'user':request.user, 'form':form})
            else:
                messages.error(request, "No dispone de permisos")
                return redirect('/')
        else:  #PARA GET
            if request.user.id == id:
                form = updateProfileForm(instance=request.user)
                return render(request, "usuario/actualizar_perfil.html", {'user':request.user, 'form':form})
            elif request.user.is_superuser:
                usuario = get_object_or_404(User, pk=id)
                form = updateProfileForm(instance=usuario)
                return render(request, "usuario/actualizar_perfil.html", {'user':request.user, 'form':form})
            else:
                messages.error(request, "No dispone de permisos")
                return redirect('/')


#Eliminar Usuairo
@login_required
def delete_user(request, id):
    if request.user.id == id or request.user.is_superuser:       
        if Pedido.objects.filter(usuario_id=id).exclude(estado='Entregado').count() == 0: #Si no tiene pedidos pendientes
           usuario =  get_object_or_404(User, pk=id)
           usuario.delete()
           messages.success(request, "Usuario eliminado correctamente")
           if request.user.is_superuser:
                return redirect("/clientes")
           return redirect('/')
        else:
            messages.error(request, "No se puede eliminar el usuario, tiene pedidos pendientes")
            return redirect('/perfil')
    else:
        messages.error(request, "No dispone de permisos")
        return redirect('/')    

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Se ha realizado el registro correctamente" )
            if request.user.is_superuser:
                return redirect("/clientes")
            login(request, user)
            return redirect("/")

        for err in form.errors.values():
            messages.error(request, err)
    form = NewUserForm()
    return render (request, 'usuario/register.html', context={"register_form":form})


def custom_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente")
    return redirect("/")




def filtrar_por_titulo(request):
    titulo = request.GET.get('titulo', '')
    libros=Libro.objects.all()
    p = re.compile(titulo.lower())
    libros = [l for l in libros if p.match(l.titulo.lower()) ]
    if(titulo != None and titulo != ''):
        return render(request,'libros/libros.html', {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})
    else:
        messages.error(request, "Introduzca un título")
        return redirect('/')




def delete_libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    if libro != None:
        if request.user.is_superuser:
            libro.delete()
            messages.success(request, "Se ha eliminado el libro correctamente" )
            return redirect('/')

        else:
            messages.error(request, "No dispone de permisos de administrador")
            return redirect('/')
    else:
        messages.error(request, "No ha introducido un libro valido")
        return redirect('/')

#Cesta
def cesta(request):
    libros=Libro.objects.all()
    return render(request, "cesta/cesta.html",   {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})



def agregar_nuevo_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Libro.objects.get(id=producto_id)
    if(producto.stock == 0):
        messages.error(request, "Este producto no tiene stock")
        return redirect('/')
    libros_diccionario = carrito.carrito.keys()
    if str(producto_id) in libros_diccionario:
        cantidad_carrito = carrito.carrito.get(str(producto_id)).get('cantidad')
    
        if(cantidad_carrito >= producto.stock):
            messages.error(request, "No hay más stock para este producto")
            return redirect('/')
        
    carrito.agregar(producto)
    messages.info(request, "Libro añadido a la cesta")
    return redirect("/")

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Libro.objects.get(id=producto_id)
    if(producto.stock == 0):
        messages.error(request, "Este producto no tiene stock")
        return redirect('/')
    libros_diccionario = carrito.carrito.keys()
    if str(producto_id) in libros_diccionario:
        cantidad_carrito = carrito.carrito.get(str(producto_id)).get('cantidad')
    
        if(cantidad_carrito >= producto.stock):
            messages.error(request, "No hay más stock para este producto")
            return redirect("Cesta")
    carrito.agregar(producto)
    messages.info(request, "Libro añadido a la cesta")
    return redirect("Cesta")

def agregar_producto_desde_detalles(request, producto_id):
    carrito = Carrito(request)
    producto = Libro.objects.get(id=producto_id)
    if(producto.stock == 0 and producto.formato == "Físico"):
        messages.error(request, "Este producto no tiene stock")
        return redirect('/')
    libros_diccionario = carrito.carrito.keys()
    if str(producto_id) in libros_diccionario:
        cantidad_carrito = carrito.carrito.get(str(producto_id)).get('cantidad')
    
        if(cantidad_carrito >= producto.stock and producto.formato == "Físico"):
            messages.error(request, "No hay más stock para este producto")
            return redirect("Cesta")
    carrito.agregar(producto)
    messages.info(request, "Libro añadido a la cesta")
    return redirect("/libro/"+str(producto_id))    

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Libro.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Cesta")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Libro.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Cesta")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Cesta")


def politica_privacidad(request):
    return render(request,'politica/privacidad.html')

    
def envios(request):
    return render(request,'politica/envios.html')

def devolucion(request):
    return render(request,'politica/devolucion.html')



def datosempresa(request):
    return render(request,'politica/datosempresa.html')

# Incidencias
def incidencias(request):
    
    if request.POST:
        form = newIncidencia(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            for err in form.errors.values():
                messages.error(request, err)
    form = newIncidencia()
    return render (request, 'incidencias/crearIncidencia.html', context={"new_incidencia_form":form})

def ver_incidencias(request):
    if request.user.is_superuser:
        incidencias=Incidencia.objects.all()
        return render(request, "administrador/verIncidencias.html",   {'datos':incidencias,'MEDIA_URL': settings.MEDIA_URL})
    else:
        messages.error(request, "No dispone de permisos de administrador")
        return redirect('/')


def filtrar_por_categoria(request, categoria_nombre):
    print("ASDASDAS")
    print(categoria_nombre)
    print([url for categoria1, url in get_categorias_choices()])
    if(categoria_nombre in [url for categoria1, url in get_categorias_choices()]):
        libros=Libro.objects.filter(categoria=categoria_nombre.replace("-"," / ").replace("_"," - "))
        if(libros.count() == 0):
            messages.info(request, "No disponemos libros de esa categoria")
            return redirect('/')
        else:

            return render(request,'libros/libros.html', {'datos':libros,'MEDIA_URL': settings.MEDIA_URL})
    else:
        print("ASDA2132sSDAS")
        messages.error(request, "No ha introducido una categoria valida")
        return redirect('/')


  
def politica_privacidad(request):
    return render(request,'politica/privacidad.html')

    
def envios(request):
    return render(request,'politica/envios.html')

def devolucion(request):
    return render(request,'politica/devolucion.html')


def datosempresa(request):
    return render(request,'politica/datosempresa.html')


from django.shortcuts import render

# Create your views here.
from django.conf import settings # new
from django.http import HttpRequest
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
import stripe
from main.Carrito import Carrito
from django.shortcuts import redirect
from django.contrib import messages
from .forms import newCustomerFormEntienda, newCustomerFormSinTienda
from main.models import Pedido, LibrosPedido,Libro
from main.context_processor import total_carrito
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage

BASE_URL = settings.BASE_URL

def hay_fisico_bro(request):
    carrito = Carrito(request)
    for item in carrito.session['carrito'].values():
            if Libro.objects.get(id=item['producto_id']).formato == "FISICO":
                return True
    return False

def enviar_correo(pedido):
    msg_isiasesio = "\n\nSi el pedido se realizó desde una cuenta esta será necesaria para ver su pedido."

    msg = ""
    libros_pedido = LibrosPedido.objects.filter(pedido=pedido)
    for item in libros_pedido:
        if Libro.objects.get(id=item.libro.id).formato == "DIGITAL":
                 msg +=  "\n- Su libro digital: {} \n {}/descarga/{}".format(item.libro.titulo, BASE_URL, item.libro.id)
    EmailMessage(
    'Gracias por su compra en Bookstore',
    'Hola {},\n\nEl pedido se ha realizado con éxito, puede seguir su pedido en:\n\n {} \n\n Direccion: {}, {} ({}) {} {}'.format(pedido.nombre, BASE_URL + '/pedido/' + str(pedido.id), pedido.direccion, pedido.localidad, pedido.provincia, msg,msg_isiasesio),
    to=[pedido.email],
    ).send()

def payment_book(request, id):
    envio = {
        'value': True,
        'payload' : 5
    }
    pedido = Pedido.objects.get(id=id)
    total_acumulado = total_carrito(request)
    if((total_acumulado['total_carrito'] > 20 or not hay_fisico_bro(request)) or pedido.en_tienda):
        envio = {
            'value': True,
            'payload' : 0
        }

    
    carrito = Carrito(request)
    return render(request, 'payment.html', {'carrito': carrito, 'pedido': pedido,'envio': envio, 'suma_total': total_acumulado['total_carrito'] + envio['payload'], 'hay_fisico': hay_fisico_bro(request)})

def parse_pedido(item):
    return {
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(item.libro.precio * 100),
                'product_data': {
                    'name': item.libro.titulo,
                },
            },
            'quantity': item.cantidad,
    }

def canceled_pedido(request):
    return render(request, 'canceled_pedido.html')

def detalles_pedido(request):
    pedido_id = request.GET.get('pedido_id')
    pedido = Pedido.objects.get(id=pedido_id)
    libros_pedido = LibrosPedido.objects.filter(pedido=pedido)

    libros_pedido = [(Libro.objects.get(id=librosp['libro_id']), librosp['cantidad'] , Libro.objects.get(id=librosp['libro_id']).precio*librosp['cantidad'] )for librosp in libros_pedido.values()] 
    total_pedido = sum([librosp[2] for librosp in libros_pedido])
    if total_pedido <= 20:
        total_pedido += 5
        libros_pedido.append(({'titulo':'Envio', 'precio': '5'}, '', 5))
    return render(request, 'detalles_del_pedido.html', {'pedido': pedido, 'libros_pedido': libros_pedido, 'total_pedido': total_pedido})

def success_pedido(request):
    try:
        Carrito(request).limpiar()
        pedido_id = request.GET.get('pedido_id')
        pedido = Pedido.objects.get(id=pedido_id)
        enviar_correo(pedido)
        pedido.fecha  = str(timezone.now().isoformat())
        pedido.session_id = request.GET.get('session_id')
        pedido.save()
        restar_item(request, pedido)
    except Exception as e:
        messages.error(request, 'No se ha podido realizar el pago')
        return redirect('/')
    return redirect('/pedido/'+ str(pedido.id))

def restar_item(request, pedido):
    libros_pedido = LibrosPedido.objects.filter(pedido=pedido)
    print(libros_pedido.values())
    for item in libros_pedido:
        libro = Libro.objects.get(id=item.libro.id)
        if(libro.stock < item.cantidad):
            messages.error(request, 'No hay suficientes libros')
            raise Exception('No hay suficientes libros')
        libro.stock -= item.cantidad
        libro.save()




def create_pedido(request):
    
    def createform(requestPost = None):
        if hay_fisico_bro(request):
            return newCustomerFormEntienda(requestPost)
        return newCustomerFormSinTienda(requestPost)
    print(HttpRequest.get_host(request))
    carrito = Carrito(request)
    if len(carrito.session['carrito'].keys()) == 0:
        messages.error(request, 'No hay productos en el carrito')
        return redirect('/')
    envio = {
        'value': True,
        'payload' : 5
    }

    total_acumulado = total_carrito(request)
    if(total_acumulado['total_carrito'] > 20 or not hay_fisico_bro(request)):
        envio = {
            'value': True,
            'payload' : 0
        }
    if request.method == "POST":
        form = createform(request.POST)
        if form.is_valid():
            pedido = form.save()
            if(request.user.is_authenticated):
                pedido.usuario = request.user
                pedido.save()
            
            for item in carrito.session['carrito'].values():
                LibrosPedido.objects.create(
                    pedido=pedido, 
                    libro = Libro.objects.get(id=item['producto_id']),
                    cantidad = item['cantidad'],)

            messages.success(request, "Se ha realizado el registro correctamente" )
            return redirect("/pedido/payment/" + str(pedido.id))
        for err in form.errors.values():
            messages.error(request, err)
    form = createform()       
    return render(request, 'create_pedido.html', {'carrito': carrito, 'form': form, 'envio': envio, 'suma_total': total_acumulado['total_carrito'] + envio['payload']})

def pago_contrareembolso(request, id):
    pedido = Pedido.objects.get(id=id)
    try:
        pedido.modo_de_pago = 'refund'
        pedido.fecha = str(timezone.now().isoformat())
        enviar_correo(pedido)
        pedido.save()
        restar_item(request, pedido)
        Carrito(request).limpiar()

    except Exception as e:
        messages.error(request, 'No se ha podido realizar el pago')
        return redirect('/')
    return redirect('/pedido/'+ str(pedido.id)) 
    # new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, id):
    pedido = Pedido.objects.get(id=id)
    libros_pedido = LibrosPedido.objects.filter(pedido=pedido)
    pedido.modo_de_pago = 'card'
    pedido.save()
    items = list(map(parse_pedido, libros_pedido))
    total_acumulado = total_carrito(request)
    if(not ((total_acumulado['total_carrito'] > 20 or not hay_fisico_bro(request)) or pedido.en_tienda)):
        items.append({
            'price_data': {
                'currency': 'eur',
                'unit_amount': 500,
                'product_data': {
                    'name': 'Envio',
                },
            },
            'quantity': 1,
        })
    
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        domain_url =BASE_URL
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/pedido/success?session_id={CHECKOUT_SESSION_ID}&pedido_id='+ str(pedido.id),
                cancel_url=domain_url + '/pedido/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=items,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

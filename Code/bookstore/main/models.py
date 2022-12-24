from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from enum import Enum
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage



fs = FileSystemStorage(location='main/')

STATE_LIST = ["Procesando", "Pagado", "Enviado", "Entregado", "En Tienda"]

def get_state_choices():
    return [(STATE_LIST[i].upper(), STATE_LIST[i]) for i in range(len(STATE_LIST))]
        
class Pedido(models.Model):

    
    numero_pedido = models.CharField(max_length=12, validators=[MinLengthValidator(12)]) # Es único: fecha+hora+4 dítidos
    direccion = models.CharField(max_length = 30, validators=[MinLengthValidator(1)])
    localidad = models.CharField(max_length = 10, validators=[MinLengthValidator(1)])
    provincia = models.CharField(max_length = 10, validators=[MinLengthValidator(1)])
    codigo_postal = models.CharField(max_length = 6, validators=[MinLengthValidator(5)])
    nombre = models.CharField(max_length = 20, validators=[MinLengthValidator(1)])
    apellidos = models.CharField(max_length = 30, validators=[MinLengthValidator(4)])
    numero_telefono = models.CharField(max_length = 9, validators=[MinLengthValidator(9)])
    email = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
    en_tienda= models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(default=STATE_LIST[0], choices=get_state_choices(), max_length=20)
    fecha = models.DateTimeField(auto_created=True, null=True, blank=True)
    modo_de_pago = models.CharField(max_length=50, null=True, blank=True, choices=[('card', 'Tarjeta de crédito'), ('refund', 'Contrareembolso')])
    session_id = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        return self.numero_pedido




categorias = ["Geografía / Turismo", "Aspectos Legales", "Ensayos / Novelas", "Textos Académicos", "Arte - Bellas Artes", "Multimedia", "Ciencia", "Bases de datos", "GNU / Linux", "Música", "Marketing / Business", "Web 2.0 y Social Media", "Otros Lenguajes", "Cómics", "SEO / SEM", "Tecnología", "Metodologías Ágiles", "Fundamentos de la Música", "Programación", "Javascript / AJAX", "Accesibilidad / Usabilidad", "CSS", "Desarrollo Web", "Cine", "MagPi", "880 Gamer", "Robótica", "Matemáticas", "Información", "Software General", "Filosofía", "HackSpace", "Ajedrez", "Historia", "Hardware", "Redes y Sys Admin", "Retroinformática", "Electrónica", "Herramientas", "Idiomas", "Educación", "Diseño / 3D", "Control de Versiones", "Atari", "Algoritmos", "Hello World"]

def parse_categoria(categoria):
    return (categoria, categoria.replace(" / ", "-").replace(" - ","_"))

def get_categorias_choices():
    return [parse_categoria(categoria) for categoria in categorias]


class elegirCategoria(Enum):
    NOVELA = "NOVELA"
    DRAMA = "DRAMA"
    ACCION = "ACCION"
    LITERARIO = "LITERARIO"
    DIDACTICO = "DIDACTICO"
    CIENTIFICO = "CIENTIFICO"
    TECNICO = "TECNICO"
    BIOGRAFICO = "BIOGRAFICO"
    AUTOBIOGRAFICO = "AUTOBIOGRAFICO"
    VIAJES = "VIAJES"
    RELIGIOSOS = "RELIGIOSOS"
    AVENTURAS = "AVENTURAS"
    HUMOR = "HUMOR"
    DEPORTE = "DEPORTE"
    CUENTO = "CUENTO"
    CIENCIA_FICCION = "CIENCIA FICCION"
    MARKETING = "MARKETING"
    SALUD = "SALUD"
    SUSPENSE = "SUSPENSE"
    VIDEOJUEGO = "VIDEOJUEGO"
    MICRORRELATO = "MICRORRELATO"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Libro(models.Model):
    titulo = models.CharField(max_length=64)
    autor = models.TextField(help_text='Autor')
    sinopsis = models.TextField(help_text='Redacta la sinopsis')
    precio = models.FloatField(help_text='Precio')
    categoria =  models.CharField(max_length=255, choices=get_categorias_choices())
    stock = models.IntegerField(help_text='Stock')
    imagen = models.ImageField(upload_to='static/images',verbose_name='Imagen', storage=fs)
    escaparate = models.BooleanField(default=False)
    formato = models.CharField(max_length=255)
    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'main_libro'


class Incidencia(models.Model):
    titulo = models.CharField(max_length=30)
    descripcion = models.TextField(help_text='Descripción de la consulta')
    nombre = models.TextField(help_text='Precio')
    apellidos =  models.TextField(help_text='Apellidos')
    nif = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    email = models.TextField(help_text='Email')
    telefono = models.CharField(max_length = 9, validators=[MinLengthValidator(9)])
    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'main_incidencia'

class LibrosPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.pedido.numero_pedido


    def __str__(self):
        return self.pedido.numero_pedido


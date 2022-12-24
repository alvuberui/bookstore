from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Libro
from .models import Incidencia
from django.contrib.auth import password_validation





class NewUserForm(UserCreationForm):
    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden"),
        "username_match": ("El nombre de usuario ya está en uso"),
        "email_match": ("Este email ya ha sido utilizado antes")
    }
    password1 = forms.CharField(
        label=("Constraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        help_text=''
    )
    password2 = forms.CharField(
        label=("Repita la contraseña"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        strip=False,
        help_text='<br></br>',
    )
    def clean_username(self):
        username = self.cleaned_data['username']
        print({username:User.objects.filter(email=username).exists()})
        
        if User.objects.filter(username=username).exists():
           raise forms.ValidationError(
                self.error_messages["username_match"],
                code="username",)
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        print({email:User.objects.filter(email=email).exists()})
        if User.objects.filter(email=email).exists():
           raise forms.ValidationError(
                self.error_messages["email_match"],
                code="match")
           
        return email
    class Meta:
        model = User
        fields=["username" ,"first_name", "last_name", "email", "password1", "password2"]

        labels = {
            'email':'Email',
            'first_name':'Nombre',
            'last_name': 'Apellidos',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

        help_texts = {
            'username':'',
        }
        
        
class updateProfileForm(UserChangeForm):
    password = None
    error_messages = {
        "username_match": ("El nombre de usuario ya está en uso"),
        "email_match": ("Este email ya ha sido utilizado antes")
    }
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
           raise forms.ValidationError(
                self.error_messages["username_match"],
                code="username",
            )
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
           raise forms.ValidationError(
                self.error_messages["email_match"],
                code="match",
            )
        return email
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
        labels = {
            'email':'Email',
            'first_name':'Nombre',
            'last_name': 'Apellidos',
            'username':'Nombre de Usuario'
        }

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'first_name': forms.TextInput(attrs={'class':'form-control mb-2  w-50 mx-auto'}),
            'last_name': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'email': forms.EmailInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
        }

        help_texts = {
            'username':''
        }
def duplicate(value):
    return (value, value)

formatos = map(duplicate,sorted(['FISICO','DIGITAL']))

class newLibro(forms.ModelForm):
    error_messages = {
        "precio_match": ("El precio debe ser mayor o igual a cero"),
        "stock_match": ("El stock debe ser mayor o igual a cero"),
    }

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
           raise forms.ValidationError(
                self.error_messages["precio_match"],
                code="precio",
            )
        return precio

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
           raise forms.ValidationError(
                self.error_messages["stock_match"],
                code="stock",
            )
        return stock
    
    class Meta:
        model = Libro
        fields = ['categoria', 'titulo', 'autor', 'sinopsis', 'precio','formato', 'stock', 'imagen', 'escaparate']
        labels = {
            'categoria':'Categoría',
            'titulo':'Título',
            'autor':'Autor',
            'sinopsis':'Sinopsis',
            'precio':'Precio',
            'stock':'Stock inicial',
            'imagen':'Imagen',
            'escaparate':'Escaparate',
            'formato':'Formato',
        }

        widgets = {
            'categoria': forms.Select(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'titulo': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'autor': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'sinopsis': forms.Textarea(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'precio': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'stock': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'imagen': forms.FileInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'escaparate': forms.CheckboxInput(attrs={'class':'form-check-input mb-2 mx-auto '}),
            'formato': forms.Select(attrs={'class':'form-control mb-2 w-50 mx-auto'}, choices=formatos),

        }

        help_texts = {
            'categoria':'',
            'titulo':'',
            'autor':'',
            'sinopsis':'',
            'precio':'',
            'stock':'',
            'imagen':'',
            'escaparate':''
        }


class UpdateLibro(forms.ModelForm):
    imagen = forms.ImageField(required=False)


    class Meta:
        model = Libro
        fields = ['categoria', 'titulo', 'autor', 'sinopsis', 'precio', 'stock', 'imagen','escaparate']
        labels = {
            'categoria':'Categoría',
            'titulo':'Título',
            'autor':'Autor',
            'sinopsis':'Sinopsis',
            'precio':'Precio',
            'stock':'Stock inicial',
            'imagen':'Imagen',
            'escaparate':'Escaparate'
            
        }

        widgets = {
            'categoria': forms.Select(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'titulo': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'autor': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'sinopsis': forms.Textarea(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'precio': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'stock': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'imagen': forms.FileInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'escaparate': forms.CheckboxInput(attrs={'class':'form-check-input mb-2 mx-auto '}),

        }

        help_texts = {
            'categoria':'',
            'titulo':'',
            'autor':'',
            'sinopsis':'',
            'precio':'',
            'stock':'',
            'imagen':'',
            'escaparate':''
        }

class newIncidencia(forms.ModelForm):
    
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'nombre', 'apellidos', 'nif', 'email', 'telefono']
        labels = {
            'titulo':'Título',
            'descripcion':'Descripción',
            'nombre':'Nombre',
            'apellidos':'Apellidos',
            'nif':'Nif',
            'email':'Email',
            'telefono':'Teléfono'
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'nombre': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'nif': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'email': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'telefono': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
        }

        help_texts = {
            'titulo':'',
            'descripcion':'',
            'nombre':'',
            'apellidos':'',
            'nif':'',
            'email':'',
            'telefono':''
        }




from django import forms


from main.models import Pedido
def duplicate(value):
    return (value.lower(), value)

provincias = map(duplicate,sorted(['Alava','Albacete','Alicante','Almería','Asturias','Avila','Badajoz','Barcelona','Burgos','Cáceres',
'Cádiz','Cantabria','Castellón','Ciudad Real','Córdoba','La Coruña','Cuenca','Gerona','Granada','Guadalajara',
'Guipúzcoa','Huelva','Huesca','Islas Baleares','Jaén','León','Lérida','Lugo','Madrid','Málaga','Murcia','Navarra',
'Orense','Palencia','Las Palmas','Pontevedra','La Rioja','Salamanca','Segovia','Sevilla','Soria','Tarragona',
'Santa Cruz de Tenerife','Teruel','Toledo','Valencia','Valladolid','Vizcaya','Zamora','Zaragoza']))
provincias2 = map(duplicate,sorted(['Alava','Albacete','Alicante','Almería','Asturias','Avila','Badajoz','Barcelona','Burgos','Cáceres',
'Cádiz','Cantabria','Castellón','Ciudad Real','Córdoba','La Coruña','Cuenca','Gerona','Granada','Guadalajara',
'Guipúzcoa','Huelva','Huesca','Islas Baleares','Jaén','León','Lérida','Lugo','Madrid','Málaga','Murcia','Navarra',
'Orense','Palencia','Las Palmas','Pontevedra','La Rioja','Salamanca','Segovia','Sevilla','Soria','Tarragona',
'Santa Cruz de Tenerife','Teruel','Toledo','Valencia','Valladolid','Vizcaya','Zamora','Zaragoza']))


# Create your models here.
class newCustomerFormEntienda(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['nombre','apellidos', 'provincia', 'direccion', 'codigo_postal','localidad', 'numero_telefono', 'email', 'en_tienda']
        labels = {
            'nombre':'Nombre',
            'apellidos':'Apellidos',
            'direccion':'Direccion',
            'localidad':'Localidad',
            'provincia':'Provincia',
            'codigo_postal':'Codigo Postal',
            'numero_telefono':'Numero Telefono',
            'en_tienda':'Recoger en tienda',
            'email':'Email'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'localidad': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'direccion': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'numero_telefono': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'provincia': forms.Select(attrs={'class':'form-control mb-2 w-50 mx-auto'} ,choices=provincias),
            'email': forms.EmailInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'en_tienda': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'codigo_postal': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'usuario': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'})
        }
        help_texts = {
            'nombre':'',
            'apellidos':'',
            'direccion':'',
            'localidad':'',
            'provincia':'',
            'numero_telefono':'',
            'en_tienda':'',
            'email':'',
        }





class newCustomerFormSinTienda(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['nombre','apellidos', 'provincia', 'direccion', 'codigo_postal','localidad', 'numero_telefono', 'email']
        labels = {
            'nombre':'Nombre',
            'apellidos':'Apellidos',
            'direccion':'Direccion',
            'localidad':'Localidad',
            'provincia':'Provincia',
            'codigo_postal':'Codigo Postal',
            'numero_telefono':'Numero Telefono',
            'email':'Email'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'localidad': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'direccion': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'numero_telefono': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'provincia': forms.Select(attrs={'class':'form-control mb-2 w-50 mx-auto'} ,choices=provincias2),
            'email': forms.EmailInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'codigo_postal': forms.NumberInput(attrs={'class':'form-control mb-2 w-50 mx-auto'}),
            'usuario': forms.TextInput(attrs={'class':'form-control mb-2 w-50 mx-auto'})
        }
        help_texts = {
            'nombre':'',
            'apellidos':'',
            'direccion':'',
            'localidad':'',
            'provincia':'',
            'numero_telefono':'',
            'email':'',
        }


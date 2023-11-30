from django import forms
from .models import Cliente, Producto

class VentaForm(forms.Form):
    # Define los campos del formulario según tus necesidades
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField()
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())

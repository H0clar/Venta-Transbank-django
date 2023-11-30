"""
URL configuration for EV4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path


from django.urls import path
from ecommerce.views import *


def base_view(request):
    return render(request, 'base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_view, name='base_view'),

    path('ver_productos/', ver_productos, name='ver_productos'),
    path('inicio/', inicio_view, name='inicio'),

    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),


    path('detalle_producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),

    path('eliminar_del_carrito/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),

    path('actualizar_carrito/<int:producto_id>/', actualizar_carrito, name='actualizar_carrito'),
    path('proceso_compra/', proceso_compra, name='proceso_compra'),

    path('api/v1/transbank/transaction/create/', transbank_create, name='transbank_create'),

    path('retorno_webpay/', retorno_webpay, name='retorno_webpay'),
    path('generar_pdf/', generar_pdf, name='generar_pdf'),

    path('generar_pdf_y_enviar_correo/', generar_pdf_y_enviar_correo, name='generar_pdf_y_enviar_correo'),

]

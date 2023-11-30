
from django.http import HttpResponseBadRequest
from .models import Cliente

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import CarritoDeCompras, Item, Producto
from django.db import transaction
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os





def ver_productos(request):
    # obten la información del carrito
    carrito_data = request.session.get('productos_seleccionados', [])

    # calcula el valor total sumando los subtotales de los productos en el carrito
    valor_total = sum(float(item['subtotal']) for item in carrito_data)

    # obtiene la lista de productos
    productos = Producto.objects.all()



    return render(request, 'ver_productos.html', {'carrito': carrito_data, 'productos': productos, 'valor_total': valor_total})




def inicio_view(request):
    return render(request, 'base.html')




def ver_carrito(request):

    # Obtén la información del carrito directamente desde la sesión
    carrito_data = request.session.get('productos_seleccionados', [])

    # Calcula el valor total sumando los subtotales de los productos en el carrito
    valor_total = sum(float(item['subtotal']) for item in carrito_data)

    # Obtén la lista de productos (puedes ajustar esta lógica según tus necesidades)
    productos = Producto.objects.all()

    # Puedes agregar lógica adicional según tus necesidades

    return render(request, 'ver_carrito.html', {'carrito': carrito_data, 'productos': productos, 'valor_total': valor_total})










def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))

        if 'productos_seleccionados' not in request.session:
            request.session['productos_seleccionados'] = []

        subtotal = producto.precio * cantidad
        request.session['productos_seleccionados'].append({
            'producto_id': str(producto.id),
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'subtotal': str(subtotal),
        })

        messages.success(request, f"{cantidad} {producto.nombre}{'s' if cantidad > 1 else ''} agregado(s) al carrito.")

        # Guarda los cambios en la sesión
        request.session.modified = True

        # Redirecciona a la página deseada después de agregar al carrito
        return redirect('ver_productos')

    return render(request, 'detalle_producto.html', {'producto': producto})



def eliminar_del_carrito(request, producto_id):
    # Obtiene la lista de productos seleccionados desde la sesión
    carrito = request.session.get('productos_seleccionados', [])

    # Busca el producto en el carrito por su ID
    for item in carrito:
        if item['producto_id'] == str(producto_id):
            # Elimina el producto del carrito
            carrito.remove(item)
            messages.success(request, f"{item['cantidad']} {item['nombre']}{'s' if item['cantidad'] > 1 else ''} eliminado(s) del carrito.")
            break

    # Actualiza la sesión con los cambios realizados en el carrito
    request.session['productos_seleccionados'] = carrito
    request.session.modified = True

    # Redirecciona a la página del carrito después de eliminar el producto
    return redirect('ver_productos')










def actualizar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))

        # Obtiene la lista de productos seleccionados desde la sesión
        carrito = request.session.get('productos_seleccionados', [])

        # Busca el producto en el carrito por su ID
        for item in carrito:
            if item['producto_id'] == str(producto.id):
                # Actualiza la cantidad y el subtotal
                item['cantidad'] = nueva_cantidad
                item['subtotal'] = str(producto.precio * nueva_cantidad)
                messages.success(request, f"Cantidad de {producto.nombre} actualizada a {nueva_cantidad}.")
                break

        # Actualiza la sesión con los cambios realizados en el carrito
        request.session['productos_seleccionados'] = carrito
        request.session.modified = True

        # Redirecciona a la página deseada después de actualizar el carrito
        return redirect('ver_productos')

    return render(request, 'ver_productos.html', {'producto': producto})













def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))

        # Crea una lista temporal en la sesión para almacenar los productos seleccionados
        if 'productos_seleccionados' not in request.session:
            request.session['productos_seleccionados'] = []

        # Agrega el producto seleccionado a la lista
        request.session['productos_seleccionados'].append({
            'producto_id': producto.id,
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'subtotal': producto.precio * cantidad,
        })

        messages.success(request, f"{cantidad} {producto.nombre}{'s' if cantidad > 1 else ''} agregado(s) al carrito.")

    return render(request, 'detalle_producto.html', {'producto': producto})










def obtener_informacion_del_carrito(request):
    carrito_data = request.session.get('productos_seleccionados', [])
    return carrito_data


def calcular_valor_total(carrito_data):
    valor_total = sum(float(item['subtotal']) for item in carrito_data)
    return valor_total


def proceso_compra(request):
    if request.method == 'POST':
        # Lógica para obtener la información del carrito
        carrito_data = obtener_informacion_del_carrito(request)

        # Calcula el valor total y otros datos necesarios
        valor_total = calcular_valor_total(carrito_data)

        try:
            # Inicia la transacción
            transaction.set_autocommit(False)

            # Realiza las operaciones necesarias con el nuevo modelo
            # (crea instancias de CarritoDeCompras, Item y Boleta)
            carrito = CarritoDeCompras.objects.create()

            for item_data in carrito_data:
                producto_id = item_data['producto_id']
                producto = get_object_or_404(Producto, id=producto_id)
                cantidad = item_data['cantidad']
                subtotal = float(item_data['subtotal'])

                item = Item.objects.create(carrito=carrito, producto=producto, cantidad=cantidad, subtotal=subtotal)

            # Limpia el carrito después de la compra
            request.session['productos_seleccionados'] = []
            request.session.modified = True

            # Commit de la transacción
            transaction.commit()

            # Agrega un print para depurar
            print("Carrito Data:", carrito_data)
            print("Valor Total:", valor_total)

            # Redirige a la página de pago de Transbank
            return render(request, 'pay_transbank.html', {'carrito': carrito_data, 'valor_total': valor_total})

        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir durante la transacción
            print("Error en la transacción:", str(e))

            # Rollback de la transacción en caso de error
            transaction.rollback()

            return HttpResponseBadRequest('Error en la transacción. Por favor, intenta nuevamente.')

        finally:
            # Restaura el modo de autocommit al valor predeterminado
            transaction.set_autocommit(True)

    # Lógica para el caso GET (si es necesario)
    carrito_data = obtener_informacion_del_carrito(request)
    valor_total = calcular_valor_total(carrito_data)

    return render(request, 'proceso_compra.html', {'carrito': carrito_data, 'valor_total': valor_total})





def header_request_transbank():
    headers = {
        "Authorization": "Token",
        "Tbk-Api-Key-Id": "597055555532",
        "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        'Referrer-Policy': 'origin-when-cross-origin',
    }
    return headers

def transbank_create(request):
    # Obtén la información del carrito directamente desde la sesión
    carrito_data = request.session.get('productos_seleccionados', [])

    # Calcula el valor total sumando los subtotales de los productos en el carrito
    montocompra = sum(float(item['subtotal']) for item in carrito_data)

    if request.method == 'POST':
        data = {
            "buy_order": "ordenCompra12345678",
            "session_id": "sesion1234557545",
            "amount": montocompra,
            "return_url": "http://localhost:8000/retorno_webpay/",
        }
        url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
        headers = header_request_transbank()
        respuesta = requests.post(url, json=data, headers=headers)

        if respuesta.status_code == 200:
            response = respuesta.json()
            newurl = response.get('url')
            tokenrs = response.get('token')
            return render(request, 'pay_transbank.html', {'url': newurl, 'token': tokenrs, 'montocompra': montocompra})
        else:
            return HttpResponse('Error al enviar la solicitud al servidor de Transbank')

    return HttpResponseBadRequest('Método no permitido')

def retorno_webpay(request):
    return render(request, 'retorno_webpay.html')








def generar_pdf(request, carrito_data):
    # Calcula el valor total sumando los subtotales de los productos en el carrito
    valor_total = sum(float(item['subtotal']) for item in carrito_data)

    # Crear un objeto PDF
    response = HttpResponse(content_type='application/pdf')

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Agregar el contenido PDF directamente sin un template
    p.drawString(100, height - 50, "Detalle del Carrito de Compra")  # Puedes personalizar esta línea

    # Agregar más contenido según tus necesidades
    y_position = height - 100  # Ajusta la posición inicial de acuerdo a tus necesidades

    # Agregar los detalles de los productos del carrito al PDF
    for item in carrito_data:
        # Asegúrate de tener imágenes asociadas a los productos o ajusta según tus necesidades
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'assets', 'images',
                                'product-item1.jpg')
        p.drawInlineImage(img_path, 100, y_position - 50, width=50, height=50)

        # Detalles del producto
        p.drawString(160, y_position, f"Producto: {item['nombre']} - Cantidad: {item['cantidad']}")
        p.drawString(160, y_position - 20, f"Subtotal: ${item['subtotal']}")

        y_position -= 70  # Ajusta el espacio entre productos según tus necesidades

    # Agregar información adicional al PDF (puedes personalizar esto según tus necesidades)
    p.drawString(100, y_position - 50 - 20, f"Valor: ${valor_total}")
    p.drawString(100, y_position - 50 - 40, "Gracias por su compra")

    p.showPage()
    p.save()

    # ruta de la carpeta contenedora del pdf
    pdf_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdf')

    # verificar si la carpeta 'pdf' existe si no pa crearla
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # guardar el PDF en la carpeta 'pdf'
    pdf_path = os.path.join(pdf_directory, 'carrito_compra.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(response.content)

    return pdf_path






def generar_pdf_y_enviar_correo(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email:

            carrito_data = request.session.get('productos_seleccionados', [])

            # generar PDF
            pdf_path = generar_pdf(request, carrito_data)

            # enviar el PDF por correo
            email_subject = 'Detalle de compra'
            email_body = 'Gracias por su compra. Adjunto el detalle de su compra.'
            from_email = 'tu@email.com'
            to_email = [email]

            email = EmailMessage(
                email_subject,
                email_body,
                from_email,
                to_email
            )

            # adjuntar el PDF al correo
            with open(pdf_path, 'rb') as pdf_file:
                email.attach('carrito_compra.pdf', pdf_file.read(), 'application/pdf')

            # enviar el correo
            email.send()

            # redirigir a la pagina ver_productos y limpiar el carrito
            request.session['productos_seleccionados'] = []
            request.session.modified = True
            return redirect('ver_productos')






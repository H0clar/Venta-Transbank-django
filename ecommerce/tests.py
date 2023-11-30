


from django.test import TestCase

from .models import CarritoDeCompras, Item, Producto, Boleta, Cliente


class CarritoCompraTestCase(TestCase):
    def setUp(self):
        # Crea un cliente asociado al usuario
        self.cliente = Cliente.objects.create(nombre='TestUser', direccion='Dirección de prueba',
                                              correo='testuser@example.com', password='testpass')

        self.producto1 = Producto.objects.create(nombre='Producto1', precio=10)
        self.producto2 = Producto.objects.create(nombre='Producto2', precio=20)

        # Crea el carrito asociado al cliente
        self.carrito = CarritoDeCompras.objects.create(cliente=self.cliente)

    def test_agregar_al_carrito(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí

    def test_eliminar_del_carrito(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí

    def test_generar_pdf_y_enviar_correo(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí

    def test_proceso_compra(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )

    def test_actualizar_carrito(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí

    def test_ver_carrito(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí

    def test_detalle_producto(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí

    def test_ver_productos(self):
        boleta_instance = Boleta.objects.create(cliente=self.cliente, total=100)
        self.item = Item.objects.create(
            carrito=self.carrito,
            boleta=boleta_instance,
            producto=self.producto1,
            cantidad=2,
            subtotal=self.producto1.precio * 2,  # Calcula el subtotal en base al precio y la cantidad
        )
        # Tus afirmaciones de prueba van aquí








class ProductoTestCase(TestCase):
    def setUp(self):
        # Crear productos de prueba
        self.producto1 = Producto.objects.create(nombre='Producto1', precio=10)
        self.producto2 = Producto.objects.create(nombre='Producto2', precio=20)

    def test_nombre_producto(self):
        # Verificar que los nombres de los productos sean correctos
        self.assertEqual(self.producto1.nombre, 'Producto1')
        self.assertEqual(self.producto2.nombre, 'Producto2')

    def test_precio_producto(self):
        # Verificar que los precios de los productos sean correctos
        self.assertEqual(self.producto1.precio, 10)
        self.assertEqual(self.producto2.precio, 20)

    def test_actualizar_precio_producto(self):
        # Actualizar el precio de un producto y verificar que se haya actualizado correctamente
        nuevo_precio = 30
        self.producto1.precio = nuevo_precio
        self.producto1.save()
        producto_actualizado = Producto.objects.get(id=self.producto1.id)
        self.assertEqual(producto_actualizado.precio, nuevo_precio)

    def test_eliminar_producto(self):
        # Eliminar un producto y verificar que ya no exista en la base de datos
        producto_a_eliminar = Producto.objects.create(nombre='ProductoEliminar', precio=15)
        producto_id = producto_a_eliminar.id
        producto_a_eliminar.delete()
        with self.assertRaises(Producto.DoesNotExist):
            Producto.objects.get(id=producto_id)









class ClienteTestCase(TestCase):
    def setUp(self):
        # Crear clientes de prueba
        self.cliente1 = Cliente.objects.create(nombre='Cliente1', direccion='Dirección1', correo='cliente1@example.com', password='pass1')
        self.cliente2 = Cliente.objects.create(nombre='Cliente2', direccion='Dirección2', correo='cliente2@example.com', password='pass2')

    def test_nombre_cliente(self):
        # Verificar que los nombres de los clientes sean correctos
        self.assertEqual(self.cliente1.nombre, 'Cliente1')
        self.assertEqual(self.cliente2.nombre, 'Cliente2')

    def test_direccion_cliente(self):
        # Verificar que las direcciones de los clientes sean correctas
        self.assertEqual(self.cliente1.direccion, 'Dirección1')
        self.assertEqual(self.cliente2.direccion, 'Dirección2')

    def test_correo_cliente(self):
        # Verificar que los correos de los clientes sean correctos
        self.assertEqual(self.cliente1.correo, 'cliente1@example.com')
        self.assertEqual(self.cliente2.correo, 'cliente2@example.com')

    def test_actualizar_direccion_cliente(self):
        # Actualizar la dirección de un cliente y verificar que se haya actualizado correctamente
        nueva_direccion = 'NuevaDirección'
        self.cliente1.direccion = nueva_direccion
        self.cliente1.save()
        cliente_actualizado = Cliente.objects.get(id=self.cliente1.id)
        self.assertEqual(cliente_actualizado.direccion, nueva_direccion)

    def test_eliminar_cliente(self):
        # Eliminar un cliente y verificar que ya no exista en la base de datos
        cliente_a_eliminar = Cliente.objects.create(nombre='ClienteEliminar', direccion='DirecciónEliminar', correo='cliente_eliminar@example.com', password='pass_eliminar')
        cliente_id = cliente_a_eliminar.id
        cliente_a_eliminar.delete()
        with self.assertRaises(Cliente.DoesNotExist):
            Cliente.objects.get(id=cliente_id)
































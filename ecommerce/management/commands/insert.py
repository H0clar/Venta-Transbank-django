import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.db import transaction
from django.utils import timezone
from ecommerce.models import Cliente, Producto, Boleta, CarritoDeCompras, Item

class Command(BaseCommand):
    help = 'Genera e inserta clientes, productos y relaciones en la base de datos'

    def handle(self, *args, **options):
        fake = Faker()

        with transaction.atomic():
            # Insertar clientes ficticios
            clientes = [Cliente(
                nombre=fake.first_name(),
                direccion=fake.address(),
                correo=fake.email(),
                password=fake.password(),  # Agregamos la contraseña ficticia
            ) for _ in range(20)]

            Cliente.objects.bulk_create(clientes)
            self.stdout.write(self.style.SUCCESS('Se han insertado 20 clientes ficticios.'))

            # Insertar productos ficticios
            productos = [Producto(
                nombre=fake.word(),
                descripcion=fake.text(),
                precio=random.uniform(10, 200),
                img=fake.image_url(),
            ) for _ in range(100)]

            Producto.objects.bulk_create(productos)
            self.stdout.write(self.style.SUCCESS('Se han insertado 100 productos ficticios.'))

            # Insertar boletas y carritos con items ficticios
            for _ in range(50):
                cliente_aleatorio = random.choice(clientes)
                boleta = Boleta(
                    cliente=cliente_aleatorio,
                    total=random.uniform(100, 1000),
                    fecha=fake.date_time_this_year(tzinfo=timezone.utc),  # Añadir información de zona horaria
                )
                boleta.save()

                carrito = CarritoDeCompras(total=boleta.total)  # Eliminamos el cliente del carrito
                carrito.save()

                items = [Item(
                    carrito=carrito,
                    boleta=boleta,
                    producto=random.choice(productos),
                    cantidad=random.randint(1, 10),
                    subtotal=random.uniform(10, 200),
                ) for _ in range(random.randint(1, 5))]

                Item.objects.bulk_create(items)

            self.stdout.write(self.style.SUCCESS('Se han insertado boletas, carritos e items ficticios.'))

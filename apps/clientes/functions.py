from apps.clientes.models import Cliente_Seguir, Compra
from apps.comercios.models import Comercio, Producto_Opinion, Comercio_Opinion

def comercios_seguidos(cliente):
	seguidos = Cliente_Seguir.objects.all().filter(cliente = cliente).values('comercio')
	
	comercios = Comercio.objects.all().filter(pk__in = seguidos)
	
	return comercios

def opino(cliente, producto):
	try:
		opinion = Producto_Opinion.objects.get(cliente = cliente, producto = producto)
		return True
	except:
		return False

def compro(cliente, producto):
	try:
		compra = Compra.objects.get(cliente = cliente, producto = producto, estado = 'recibido')
		return True
	except:
		return False

def opino_comercio(cliente, comercio):
	try:
		opinion = Comercio_Opinion.objects.get(cliente = cliente.id, comercio = comercio.id)
		return True
	except:
		return False
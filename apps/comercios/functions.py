
from apps.clientes.models import Cliente_Seguir
from apps.comercios.models import Comercio

def YaSeguido(comercio, cliente):
	try:
		seguir = Cliente_Seguir.objects.get(comercio = comercio, cliente = cliente)
	except:
		seguir = False

	if seguir:
		return True
	else:
		return False



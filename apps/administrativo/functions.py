#encoding:utf-8
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import LoginForm
from apps.comercios.models import Comercio, Producto, Publicacion
from apps.clientes.models import Cliente, Compra
from .models import Usuario, Notificacion

import re


def get_related_dasboard_url(usuario):
	try:
		cliente = Cliente.objects.get(usuario = usuario.id)
	except:
		cliente = None

	try: 
		comercio = Comercio.objects.get(usuario = usuario.id)
	except:
		comercio = None

	if cliente:
		return redirect('client_app:DashBoard')
	if cliente == None:
		return redirect('comerce_app:DashBoard')


def LogIn(request, username, password):
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			usuario = Usuario.objects.get(username = user.username)
			return get_related_dasboard_url(usuario)
			
	else:
		login_form = LoginForm(request.POST)
		mensaje = "Los datos ingresados no son validos"
		return render (request, 'administrativo/login.html', {'login_form' : login_form, 'mensaje' : mensaje})


def normalize_query(texto_busqueda, terminos_busqueda=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
	''' Divide la cadena de consulta en palabras claves individuales, deshaciendose de los espacios innecesarios y agrupando palabras citadas.
	    ejempo:

	    >>> normalize_query('  algunas palabras aleatorias "con citas" y      espacios')
	    ['alunas', 'palabras', 'aleatorias', 'con citas', 'y', 'espacios']

	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in terminos_busqueda(texto_busqueda)]

def get_query(texto_busqueda, campos_busqueda, modelo):
	''' Retorna una consulta, una lista de X modelo recibido, consulta realizada por cada termino recibido como argumento, en los campos de busqueda recibidos como argumento.

	'''
	query = None         
	terminos = normalize_query(texto_busqueda)
	for termino in terminos:
	    or_query = None 
	    for nombre_campo in campos_busqueda:
	        q = modelo.objects.filter(**{"%s__icontains" %nombre_campo : termino})
	        #si es la primera ver que se busca el termino or_query esta vacio, entonces se le asigna q(query encontrado)
	        if or_query is None:
	            or_query = q
		       #si no, quiere decir que es el segundo campo que buscamos, entonces or_query no esta vacio, y por ende se le adiciona q(query encontrado)		        
	        else:
	            or_query = or_query | q
	            
	    #si es la primera vez que buscamos el termino entonces query esta vacio, por ende se le asigna or_query(lista de objetos econtrados)
	    if query is None:
	        query = or_query
	        #si no, quiere decir que es el segundo termino que buscamos, y por ende, query no esta vacio, entonces se le adiciona or_query(lista de objetos encontrados)
	    else:
	        query = query & or_query
	return query

def enviar_notificacion(modelo, accion, relacionado, destinatario):

	
	#El relacionado es quien realiza la accion (Cliente o comercio)
	#El Modelo es quien "recibe" la accion (Publicacion, Producto, Compra)
	dicc = {
	'comentario' : '%s ha realizado un comentario en tu publicación, %s.',
	'pregunta' : '%s ha realizado una pregunta en tu producto, %s',
	'respuesta' : '%s ha respondido tu prengunta en el producto, %s',
	'compra' : '%s ha comprado el producto, %s',
	'pago' : '%s ha realizado el pago del producto, %s',
	'enviado' : '%s ha eviado tu producto, %s',
	'recibido' : '%s ha recibido el producto, %s',
	'registroComercio' : '¡Los primeros 3 meses los regala la casa!, al inicio del 4to mes se reanudará el cobro por el servicio.',
	'reciboAutomatico' : 'Se a generado un recibo automatico debido al vencimiento del recibo nro %s.',
	'valorarProducto' : '%s ha valorado el producto comprado, %s.',
	'valorarComercio' : '%s te ha valorado como comercio.'
	}
	if modelo.__class__.__name__ == 'Publicacion':		
		descripcion = dicc[accion]%(relacionado.nombre, modelo.titulo)
	if modelo.__class__.__name__ == 'Compra':
		descripcion = dicc[accion]%(relacionado.nombre, modelo.producto.nombre)
	if modelo.__class__.__name__ == 'Producto':
		descripcion = dicc[accion]%(relacionado.nombre, modelo.nombre)
	if modelo.__class__.__name__ == 'Comercio':
		descripcion = dicc[accion]%(relacionado.nombre)
	if modelo.__class__.__name__ == 'Recibo':
		descripcion = dicc[accion]

	url = None

	if modelo.__class__.__name__ == 'Publicacion':
		url = '/comercios/ver_publicacion/%s/' %(modelo.id)
	if modelo.__class__.__name__ is 'Producto':
		url = '/comercios/ver_producto/%s/' %(modelo.id)
	if modelo.__class__.__name__ is 'Compra' and destinatario.__class__.__name__ is 'Comercio':
		url = '/comercios/ver_compra/%s/' %(modelo.id)
	if modelo.__class__.__name__ is 'Compra' and destinatario.__class__.__name__ is 'Cliente':
		url = '/clientes/pagar/%s/' %(modelo.id)
	if modelo.__class__.__name__ is 'Comercio':
		url = '/comercios/ver_comercio/%s/' %(modelo.id)
	if modelo.__class__.__name__ is 'Recibo':
		url = '/ver_recibo/%s/' %(modelo.id)

	Notificacion.objects.create(
		modelo = modelo.__class__.__name__, 
		id_modelo = modelo.id, 
		descripcion = descripcion, 
		relacionado = relacionado.__class__.__name__, 
		id_relacionado = relacionado.id, 
		url = url,
		destinatario = destinatario.__class__.__name__,
		id_destinatario = destinatario.id
		)


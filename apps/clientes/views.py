#encoding:utf-8
"""
	Plataforma comercial para la Promocion, Publicidad y Ventas de Productos en linea para las empresas del Municipio Juan German Roscio, Estado Guarico.
	Autor: David Abreu
"""

""" 
	DEFINICION:

	En esta seccion del sistema se realizan toda la parte relacionada a la logica de negocios del sistema,
	tales como consultas a la base de datos, renderizacion de templates, y acciones relacionadas al CRUD del
	modulo de clientes.
"""

"""
	En la siguiente seccion de codigo se realizan todas las importaciones de paquetes relacionadas
	directamente con el framework
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
#Se importan las vistas genericas basasdas en clases de Django 
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
#Se importan los paquetes necesarios de Django-Braces
from braces.views import LoginRequiredMixin
from django.utils import timezone



"""
	En la siguiente seccion se importan los paquetes relacionados al sistema en cuestion
"""
from .forms import CompraForm, CompraEnvioForm, CompraPagoForm
from .models import Compra, Cliente, Cliente_Seguir
from apps.comercios.models import Producto, Producto_Fotos, Publicacion, Comercio, Producto_Opinion
from apps.comercios.forms import ProductoOpinionForm, ComercioOpinionForm
from apps.administrativo.models import Area_Interes, Notificacion
from .functions import comercios_seguidos, opino, compro
from apps.administrativo.functions import enviar_notificacion

"""
	Funcion ComprarProducto:
	Vista basada en funcion que muestra un formulario para la compra de un producto, y, cuando la peticion es post valida y procesa la informacion para luego redirigir al usuario al formulario de pago, con la informacion de compra guardada.
	Variables:
		producto
		compraF
		envioF
		compra
		envio
		producto
		productoFotos
		context
"""
def ComprarProducto(request, pk):
	#Se intenta obtener el producto con el id recibido, si no retorna 404
	producto = get_object_or_404(Producto, pk = pk)

	#si la peticion es POST se inicia el proceso de validacion y guardado
	if request.method == "POST":
		#Se asignan a las variables los datos obtenidos del formulario
		compraF = CompraForm(request.POST)
		envioF = CompraEnvioForm(request.POST)

		#Se comprueba que el usuario no haya seleccionado una cantidad mayor a la existencia del producto a comprar...
		if int(compraF.data['cantidad']) > producto.stock:
			#... de hacerlo se agrega un error al formulario
			compraF.add_error(None, 'Has ingresado una cantidad mayor a la existente')
			#se envia el formulario de compra y de envio junto con las fotos como variable de contexto nuevamente al template de compra del producto
			envioF = CompraEnvioForm(request.POST)
			productoFotos = Producto_Fotos.objects.get(producto=producto.id)
			context = {
				'CompraForm' : compraF,
				'EnvioForm' : envioF,
				'producto' : producto,
				'productoFotos' : productoFotos
			}
			return render(request, 'clientes/compras/comprar.html', context)

		#si el usuario selecciona envio a direccion como tipo de entrega
		#Se validan los formularios de envio y de compra
		if (compraF.data['tipo_entrega'] == 'envio') and (compraF.is_valid() and envioF.is_valid()):

			#se crea un objeto de tipo Compra con los datos recibidos por el formulario
			compra = compraF.save(commit=False)
			#se crea un objeto de tipo Compra_Envio con los datos recibidos por el formulario			
			envio = envioF.save(commit=False)
			print(envio.direccion)
			if envio.direccion == "":
				envio.direccion = request.user.cliente.direccion

			#se relaciona la compra con el cliente
			compra.cliente = request.user.cliente
			#se relaciona la compra con el comercio
			compra.comercio = producto.Comercio
			#se relaciona la compra con el producto
			compra.producto = producto
			#primeramente se guarda en la BDD el objeto de tipo Compra_Envio para obtener su id
			envio.save()
			#luego se relaciona el objeto de tipo Compra_Envio con la respectiva Compra
			compra.envio = envio
			#se guarda el objeto de tipo Compra en la BDD
			compra.save()
			producto.stock -= compra.cantidad
			producto.save()
			enviar_notificacion(compra, 'compra', request.user.cliente, compra.comercio)

			return redirect('client_app:PagarCompra', pk=compra.id)
		#si no: el cliente seleccionó el tipo de entrega personal, por lo que solo se valida el formulario de compra
		elif compraF.data['tipo_entrega'] == 'personal' and compraF.is_valid():
			#se crea un objeto de tipo Compra con los datos recibidos por el formulario
			compra = compraF.save(commit=False)
			#se relaciona la compra con el cliente
			compra.cliente = request.user.cliente
			#se relaciona la compra con el comercio
			compra.comercio = producto.Comercio
			#se relaciona la compra con el producto
			compra.producto = producto
			#se guarda el objeto de tipo Compra en la BDD
			compra.save()
			producto.stock -= compra.cantidad
			producto.save()
			enviar_notificacion(compra, 'compra', request.user.cliente, compra.comercio)
			return redirect('client_app:PagarCompra', pk=compra.id)
		#en ninguno de los cosas se devuelven los formularios con sus respectivos errores, junto con las fotos del producto
		#a la vista comprar
		else:
			compraF = CompraForm(request.POST)
			envioF = CompraEnvioForm(request.POST)
			productoFotos = Producto_Fotos.objects.get(producto=producto.id)
			context = {
				'CompraForm' : compraF,
				'EnvioForm' : envioF,
				'producto' : producto,
				'productoFotos' : productoFotos
			}

			return render(request, 'clientes/compras/comprar.html', context)
	#si la peticion no es post se envian instacias de formularios, con las fotos del producto en una variable de contexto
	#al template
	productoFotos = Producto_Fotos.objects.get(producto=producto.id)
	compraF = CompraForm
	envioF = CompraEnvioForm
	context = {
		'CompraForm' : compraF,
		'EnvioForm' : envioF,
		'producto' : producto,
		'productoFotos' : productoFotos
	}

	return render(request, 'clientes/compras/comprar.html', context)

"""
	Funcion PagarProducto:
		Funcion que recibe como argumento la compra a pagar, devolviendo los datos de la compra siempre y cuando coincida con el cliente que esta logueado.
		Cuando el metodo es POST hace las validaciones para guardar los datos del pago
"""
def PagarProducto(request, pk):
	#se intenta obtener objeto de tipo "compra", con el pk recibido, y el id del cliente
	#se asigna a la varible, de no tener exito se devuelve error 404
	compra = get_object_or_404(Compra, pk = pk, cliente = request.user.cliente.id)

	#se el metodo es POST se hacen las validaciones, se guarda en la BDD y se relaciona el pago con la compra
	if request.method == "POST":
		pagoF = CompraPagoForm(request.POST)

		if not compra.envio:
			compra.estado = 'recibido'
			compra.save()
			enviar_notificacion(compra, 'pago', request.user.cliente, compra.comercio)
		if compra.envio and pagoF.is_valid():
			pago = pagoF.save(commit=False)
			pago.save()
			compra.estado = 'pagado'
			compra.pago = pago
			compra.save()
			enviar_notificacion(compra, 'pago', request.user.cliente, compra.comercio)
		else:
			pagoF = CompraPagoForm(request.POST)
			context = {
				'PagoForm' : pagoF,
				'compra' : compra,
				'fotos' : Producto_Fotos.objects.get(producto=compra.producto.id)
			}
			return render(request, 'clientes/compras/pagar.html', context)

	#si la solicitud no es POST, se envian las variables de entorno y se renderiza el template
	pagoF = CompraPagoForm
	if opino(request.user.cliente, compra.producto) == False:
		context = {
			'PagoForm' : pagoF,
			'compra' : compra,
			'fotos' : Producto_Fotos.objects.get(producto=compra.producto.id),
			'opinionForm' : ProductoOpinionForm(),
			'producto' : compra.producto
		}
		return render(request, 'clientes/compras/pagar.html', context)
	context = {
		'PagoForm' : pagoF,
		'compra' : compra,
		'fotos' : Producto_Fotos.objects.get(producto=compra.producto.id)
	}
		

	return render(request, 'clientes/compras/pagar.html', context)

def RecibirProducto(request, pk):
	compra = get_object_or_404(Compra, pk = pk)
	if request.method == "POST":
		compra.estado = 'recibido'
		compra.save()
		enviar_notificacion(compra, 'recibido', request.user.cliente, compra.comercio)
		return redirect('client_app:PagarCompra', compra.id)

class DashBoard(LoginRequiredMixin, TemplateView):

	login_url = 'principal:login'

	template_name = 'clientes/dashboard/index.html'

	def get_context_data(self, **kwargs):
		context = super(DashBoard, self).get_context_data(**kwargs)
		context['cliente'] = get_object_or_404(Cliente, pk = self.request.user.cliente.id)

		#productos y publicaciones de los comercios a los que sigue el usuario
		comerciosSeguidos = comercios_seguidos(self.request.user.cliente.id)
		try:
			context['productosSeguidos'] = Producto.objects.all().filter(
					activo = True, 
					Comercio__in = comerciosSeguidos
			)
		except:
			context['productosSeguidos'] = Producto.objects.all().filter(
					activo = True, 
					Comercio = comerciosSeguidos
			)

		context['productoFotosSeguidos'] = Producto_Fotos.objects.all().filter(producto__in = context['productosSeguidos'])
		context['publicacionesSeguidos'] = Publicacion.objects.all().filter(activo = True, comercio__in = comerciosSeguidos)
		#productos y publicaciones de las areas de interes del usuario
		context['productosAreas'] = Producto.objects.all().filter(area_interes__in=self.request.user.cliente.area_interes.all())
		context['productoFotosAreas'] = Producto_Fotos.objects.all().filter(producto__in = context['productosAreas'])
		context['publicacionesAreas'] = Publicacion.objects.all().filter(activo = True, area_interes__in=self.request.user.cliente.area_interes.all())


		#compras pendientes del usuario
		context['comprasPendientes'] = Compra.objects.all().filter(cliente = self.request.user.cliente.id).exclude(estado = 'recibido')
		context['comprasConcretadas'] = Compra.objects.all().filter(estado = 'recibido', cliente = self.request.user.cliente.id)
		context['notificaciones'] = Notificacion.objects.all().filter(destinatario = 'Cliente', id_destinatario = self.request.user.cliente.id).order_by('-fecha_reg')
		context['sinLeer'] = Notificacion.objects.all().filter(destinatario = 'Cliente', id_destinatario = self.request.user.cliente.id, leido = False).count()

		return context

def SeguirComercio(request, pkCli, pkCo):
	if request.method == 'POST':
		cliente = Cliente.objects.get(pk = pkCli)		
		comercio = Comercio.objects.get(pk = pkCo)
		Cliente_Seguir.objects.create(cliente = cliente, comercio = comercio)
		return redirect ('comerce_app:VerComercio', pk = pkCo)

def ValorarProducto(request, pkPro):
	if request.method == "POST":
		opinionForm = ProductoOpinionForm(request.POST)
		if opinionForm.is_valid():
			producto = Producto.objects.get(pk = pkPro)
			

			opinion = opinionForm.save(commit=False)
			opinion.cliente = request.user.cliente
			opinion.producto = producto
			opinion.puntaje = request.POST.get('puntaje')
			opinion.save()
			enviar_notificacion(producto, 'valorarProducto', request.user.cliente, producto.Comercio)
			return redirect('comerce_app:VerProducto', producto.id)
	return redirect('comerce_app:VerProducto', producto.id)

def ValorarComercio(request, pkCo):
	if request.method == "POST":
		opinionForm = ComercioOpinionForm(request.POST)
		if opinionForm.is_valid():
			comercio = Comercio.objects.get(pk = pkCo)

			opinion = opinionForm.save(commit=False)
			opinion.cliente = request.user.cliente
			opinion.comercio = comercio
			opinion.puntaje = request.POST.get('puntaje')
			opinion.save()
			enviar_notificacion(comercio, 'valorarComercio', request.user.cliente, comercio)
			return redirect('comerce_app:VerComercio', comercio.id)			
	return redirect('comerce_app:VerComercio', comercio.id)
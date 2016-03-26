#encoding:utf-8
"""
	Plataforma comercial para la Promocion, Publicidad y Ventas de Productos en linea para las empresas del Municipio Juan German Roscio, Estado Guarico.
	Autor: David Abreu
"""

""" 
	DEFINICION:

	En esta seccion del sistema se realizan toda la parte relacionada a la logica de negocios del sistema,
	tales como consultas a la base de datos, renderizacion de templates, registro de usuarios, comercios clientes, y la seccion pricipal del sistema. 
"""

"""
	En la siguiente seccion de codigo se realizan todas las importaciones de paquetes relacionadas
	directamente con el framework
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import logout
from datetime import datetime, timedelta

"""
	En la siguiente seccion se importan los paquetes relacionados al sistema en cuestion
"""
#Se importan los modelos de la app Administrativo
from .models import Area_Interes, Usuario, PagoRecibo, Recibo, Notificacion
#Se importan los moldelos de la apps Cliente
from apps.clientes.models import Cliente 
#se importan los modelos de la App comercio
from apps.comercios.models import Producto, Comercio, Producto_Fotos, Publicacion, Publicacion_Comentario 
#Se importan los formularios necesarios
from .forms import LoginForm, RegistroUsuarioForm, RegistroComercioForm, RegistroClienteForm, ComercioTelefonoForm, PagoReciboForm
#Se importan las funciones necesarias
from .functions import LogIn, get_query, enviar_notificacion
from braces.views import LoginRequiredMixin


class IndexView(TemplateView):

	template_name = 'administrativo/index.html'


	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['areas'] = Area_Interes.objects.all()
		context['num'] = [11, 21, 31, 41]
		if 'area' in self.request.GET:
			area = self.request.GET.get('area', False)
			context['publicaciones'] = Publicacion.objects.all().filter(activo=True, area_interes = area)
			context['productos'] = Producto.objects.all().filter(activo=True, area_interes = area)			
			context['fotos'] = Producto_Fotos.objects.all().filter(producto__in = context['productos'])
			context['filtro'] = True
			context['area'] = Area_Interes.objects.get(pk = area)
			if context['productos'].count() == 0:
				context['mensaje'] = "Lo sentimos, no hay ningún producto aún en el Área de Interés que seleccionaste."
			if context['publicaciones'].count() == 0:
				context['mensaje'] = "Lo sentimos, no hay ninguna publicación aún en el Área de Interés que seleccionaste."
		else:
			context['publicaciones'] = Publicacion.objects.all().filter(activo=True)			
			context['productos'] = Producto.objects.all().filter(activo=True)
			context['fotos'] = Producto_Fotos.objects.all().filter(producto__in = context['productos'])
		return context

	
def Login(request):
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			return LogIn(request, login_form.cleaned_data['username'],
					login_form.cleaned_data['password'])
			
	else:
		login_form = LoginForm()
	return render (request, 'administrativo/login.html', {'login_form' : login_form})

def Logout(request):
	logout(request)
	return redirect('/')
"""
	La siguiente funcion se encarga del registro del Comercio junto el su Usuario de manera simultanea,
	validando que los datos obtenidos sean validos, guardando el usuario y posteriormente el Comercio 
	relacionandolo con la informacion del Usuario guardada
"""


def RegistroComercio(request):
	if request.method == "POST":
		#Se asigna a las variables los datos obtenidos desde el formulario
		datosUsuario = RegistroUsuarioForm(request.POST, prefix='usuario')
		datosComercio = RegistroComercioForm(request.POST, request.FILES, prefix='comercio')
		datosTelefono = ComercioTelefonoForm(request.POST, prefix='telefono')
		#Se verifica la valides de los formularios
		if datosComercio.is_valid() and datosUsuario.is_valid() and datosTelefono.is_valid():

			#Se crea el usuario con los datos recibidos
			Usuario.objects.create_user(username= datosUsuario.cleaned_data['username'],
											email = datosUsuario.cleaned_data['email'],
											password = datosUsuario.cleaned_data['password']
											)
			#Se crea un objeto Usuario con el Usuario recien guardado
			usuario = Usuario.objects.get(username = datosUsuario.cleaned_data['username'])

			#Se crea un objeto Comercio con los datos del formulario
			nuevoComercio = datosComercio.save(commit=False)
			#Se relaciona el usuario con el comercio
			nuevoComercio.usuario = usuario
			#Se guarda el objeto Comercio en la BDD
			nuevoComercio.save()

			#Se guarda la realcion de muchos a muchos existente en el formulario (Area_interes)
			datosComercio.save_m2m()

			#Se obtienen los datos telefonicos
			telefonoComercio = datosTelefono.save(commit=False)
			#se relaciona el modelo Comercio_Telefono, con el Comercio
			telefonoComercio.comercio = nuevoComercio
			#Se guarda en la base de datos
			telefonoComercio.save()

			#Se crea el primer recibo para el comercio
			Recibo.objects.create(comercio = nuevoComercio, fecha_fin = datetime.now() + timedelta(weeks=13), descripcion = "3 Meses que paga la Casa.", precio = 90000, estado = 'pagado')

			#Se envia la notificacion al comercio del nuevo recibo
			recibo = Recibo.objects.get(comercio = nuevoComercio)
			PagoRecibo.objects.create(recibo = recibo, fecha_pago = datetime.now(), nro_referencia= 0000, precio = 90000)
			enviar_notificacion(recibo, 'registroComercio', nuevoComercio, nuevoComercio )



			LogIn(request, datosUsuario.cleaned_data['username'], datosUsuario.cleaned_data['password'])
			#return redirect('/')
		else:
			context = {
				'UsuarioForm' : datosUsuario,
				'ComercioForm' : datosComercio,
				'TelefonoForm' : datosTelefono
			}
			return render(request, 'administrativo/registro_comercio.html', context)

	#Si no se recibe ningun metodo post, se envia como contexto el formulario y el template
	context = {
		'UsuarioForm' : RegistroUsuarioForm(prefix='usuario'),
		'ComercioForm' : RegistroComercioForm(prefix='comercio'),
		'TelefonoForm' : ComercioTelefonoForm(prefix='telefono')

	}
	return render(request, 'administrativo/registro/registro_comercio.html', context)


def RegistroCliente(request):
	if request.method == "POST":
		#Se asigna a las variables los datos obtenidos desde el formulario
		datosUsuario = RegistroUsuarioForm(request.POST, prefix='usuario')
		datosCliente = RegistroClienteForm(request.POST, request.FILES, prefix='cliente')
		#Se verifica la valides de los formularios
		if datosCliente.is_valid() and datosUsuario.is_valid():
			#Se crea el usuario con los datos recibidos
			Usuario.objects.create_user(username= datosUsuario.cleaned_data['username'],
											email = datosUsuario.cleaned_data['email'],
											password = datosUsuario.cleaned_data['password']
											)
			#Se crea un objeto Usuario con el Usuario recien guardado
			usuario = Usuario.objects.get(username = datosUsuario.cleaned_data['username'])
			#Se crea un objeto cliente con los datos del formulario
			nuevoCliente = datosCliente.save(commit=False)
			#Se relaciona el usuario con el cliente
			nuevoCliente.usuario = usuario
			#Se guarda el objeto cliente en la BDD
			nuevoCliente.save()
			#Se guarda la relacion mucho a muchos existente en el formulario (area_interes)
			datosCliente.save_m2m()
			LogIn(request, datosUsuario.cleaned_data['username'], datosUsuario.cleaned_data['password'])
			#return redirect('/')
		else:
			context = {
			'UsuarioForm' : datosUsuario,
			'ClienteForm' : datosCliente
		}

	#Si no se recibe ningun metodo post, se envia como contexto el formulario y el template
	context = {
		'UsuarioForm' : RegistroUsuarioForm(prefix='usuario'),
		'ClienteForm' : RegistroClienteForm(prefix='cliente')
	}
	return render(request, 'administrativo/registro/registro_cliente.html', context)

def Buscar(request):

	if request.GET.get('texto') and request.GET.get('texto').strip():
		 
		#publicaciones
		campos_busqueda = ('titulo', 'contenido', 'comercio__nombre')
		texto_busqueda = request.GET.get('texto')
		publicaciones = get_query(texto_busqueda, campos_busqueda, Publicacion)
		
		#comercios
		campos_busqueda = ('nombre'),
		comercios = get_query(texto_busqueda, campos_busqueda, Comercio)

		#productos
		campos_busqueda = ('nombre', 'Comercio__nombre', 'descripcion_corta', 'descripcion')
		productos = get_query(texto_busqueda, campos_busqueda, Producto)
		fotos = Producto_Fotos.objects.all().filter(producto__in=productos)

		context = {
			'productos' : productos,
			'publicaciones' : publicaciones,
			'comercios' : comercios,
			'fotos' : fotos
		}
		return render(request, 'administrativo/resultados.html', context)


	
	return redirect('comerce_app:ListarProductos')

class Productos(TemplateView):
	#Se indica el template a renderizar
	template_name = 'administrativo/productos.html'
	
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(Productos, self).get_context_data(**kwargs)
		#se asigna a la variable de contexto todos los productos relacionados con el comercio logueado
		context['productos']=Producto.objects.all().filter(activo = True)
		
		#se asigna a la variable de contexto todos las fotos relacionadas a los productos con el comercio logueado
		context['fotos'] = Producto_Fotos.objects.all().filter(producto__in=context['productos'])
		context['areas'] = Area_Interes.objects.all()
		context['num'] = [11, 21, 31, 41]	
		
		#se retorna la variable de contexto
		return context

class Publicaciones(TemplateView):
	#Se asigna el template a utilizar
	template_name = 'administrativo/publicaciones.html'
	
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(Publicaciones, self).get_context_data(**kwargs)		
		#Se obtienen las publicaciones del comercio logeado
		context['publicaciones']=Publicacion.objects.all()
		#Se obtienen los comentarios de las publicaciones del comercio logeado
		context['comentarios']=Publicacion_Comentario.objects.all()
		context['areas'] = Area_Interes.objects.all()
		context['num'] = [11, 21, 31, 41]
		#se retorna la variable de contexto
		return context

class Comercios(TemplateView):
	#Se asigna el template a utilizar
	template_name = 'administrativo/comercios.html'
	
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(Comercios, self).get_context_data(**kwargs)		
		context['comercios'] = Comercio.objects.all().filter(activo = True)
		return context

class VerRecibo(LoginRequiredMixin, DetailView):
	login_url = 'principal:login'
	model = Recibo
	template_name = 'administrativo/recibos/ver_recibo.html'
	context_object_name = 'recibo'
	def get_context_data(self, **kwargs):
		context = super(VerRecibo, self).get_context_data(**kwargs)	
		try:
			recibo = context['recibo']
			context['pagoRecibo'] = PagoRecibo.objects.get(recibo = recibo)
		except:
			context['pagoReciboForm'] = PagoReciboForm()
		return context

class ListarRecibos(LoginRequiredMixin, TemplateView):
	login_url = 'principal:login'
	template_name= 'administrativo/recibos/listar_recibos.html'
	def get_context_data(self, **kwargs):
		context = super(ListarRecibos, self).get_context_data(**kwargs)	
		context['recibosPendientes'] = Recibo.objects.all().filter(comercio = self.request.user.comercio).exclude(estado = 'pagado')			
		context['recibosCancelados'] = Recibo.objects.all().filter(comercio = self.request.user.comercio, estado = 'pagado')
		context['pagoRecibos'] = PagoRecibo.objects.all().filter(recibo__in= context['recibosCancelados'])
		return context
	
def PagarRecibo(request, pk):
	if request.method == 'POST':
		recibo = get_object_or_404(Recibo, pk = pk)

		pagoForm = PagoReciboForm(request.POST)

		#se verifica que la cantidad cancelada corresponda a la cantidad de meses seleccionados
		total = int(pagoForm.data['meses']) * 30000
		if int(pagoForm.data['precio']) != total:
			pagoForm.add_error(None, 'El total cancelado no corresponde con la cantidad de meses seleccionados')
			context = {
				'recibo' : recibo,
				'pagoReciboForm' : pagoForm
			}
			return render(request, 'administrativo/recibos/ver_recibo.html', context)
		#se verifica la valides del formulario
		if pagoForm.is_valid() and int(pagoForm.data['precio']) == total:
			fecha_fin = datetime.now() + timedelta(weeks=(int(pagoForm.data['meses']) * 4.34524))
			recibo.fecha_fin = fecha_fin
			recibo.estado = 'por verificar pago'
			recibo.save()

			pago = pagoForm.save(commit=False)
			pago.recibo = recibo
			pago.save()
			return redirect('principal:VerRecibo', pk = pk)
		else:
			context = {
				'recibo' : recibo,
				'pagoReciboForm' : pagoForm
			}
			return render(request, 'administrativo/recibos/ver_recibo.html', context)
	return redirect('principal:VerRecibo', pk)



def VerNotificacion(request, pk):
	if request.method == "POST":
		notificacion = get_object_or_404(Notificacion, pk = pk)
		if notificacion.leido == False:
			notificacion.leido= True
			notificacion.save()
		return redirect(notificacion.url)

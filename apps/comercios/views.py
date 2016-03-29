#encoding:utf-8
"""
	Plataforma comercial para la Promocion, Publicidad y Ventas de Productos en linea para las empresas del Municipio Juan German Roscio, Estado Guarico.
	Autor: David Abreu
"""

""" 
	DEFINICION:

	En esta seccion de codigo se realiza toda la parte relacionada a la logica de negocios,
	tales como consultas a la base de datos, renderizacion de templates, y acciones relacionadas al CRUD del
	modulo de comercios.
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

"""
	En la siguiente seccion se importan los paquetes relacionados al sistema en cuestion
"""
#Se importan los formularios a utilizar
from .forms import NuevoProductoForm, ProductoFotosForm, PublicacionForm, PublicacionComentarioForm, ProductoPreguntaForm, ProductoRespuestaForm, ProductoOpinionForm, ComercioOpinionForm
#Se importan los modelos a utilizar
from .models import Comercio, Producto, Producto_Fotos, Publicacion, Publicacion_Comentario, Producto_Pregunta, Producto_Respuesta, Producto_Opinion, Comercio_Opinion
from .functions import YaSeguido
from apps.clientes.models import Compra, Compra_Pago, Compra_Envio
from apps.clientes.functions import opino, compro, opino_comercio
from apps.administrativo.functions import enviar_notificacion
from apps.administrativo.models import Notificacion

"""
	INFORMACION GENERAL:
	El mixin 'LoginRequiredMixin', asginado como argumento a la mayoria de las  clases del algoritmo
	es utilizado para indicar que se requiere el logeo del usuario para el acceso a dicha funcion o clase.

	El atributo 'login_url' dentro de cada funcion o clase es propio de LoginRequiredMixin, e indica la url 
	a la cual rediccionará al usuario para que se logee al sistema.
"""

"""
	Clase DashBoard:
	La siguiente clase, llamada 'DashBoard', tablero de instrumentos al español, corresponde al ADV Perfil del comercio.
	Se encarga de consultar toda la informacion referente al comercio para ser mostrada en el perfil del mismo.

	Variables:
		login_url
		template_name
		context
"""
class DashBoard(LoginRequiredMixin, TemplateView):

	login_url = 'principal:login'

	#Se indica el template a renderizar
	template_name = 'comercios/dashboard/index.html'
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(DashBoard, self).get_context_data(**kwargs)
		#se asigna a la variable de contexto todos los productos relacionados con el comercio logueado
		context['productos']=Producto.objects.all().filter(Comercio = self.request.user.comercio.id, activo=True)
		#se asigna a la variable de contexto todos las publicaciones relacionados con el comercio logueado
		context['publicaciones']=Publicacion.objects.all().filter(comercio = self.request.user.comercio.id, activo=True)		
		#se asigna a la variable de contexto todos las fotos relacionadas a los productos con el comercio logueado
		context['fotos'] = Producto_Fotos.objects.all().filter(producto__Comercio = self.request.user.comercio.id)
		"""
			Como funciona la consulta de la variable context['fotos']:

			El modelo Producto_Fotos contiene una llave foranea llamada 'producto' al modelo Producto, el cual posee
			una llave foranea al modelo comercio llamada 'Comercio'.

			En la consulta se filtran las fotos las cuales su relacionado(Producto), contenga una llave foranea a su 
			relacionado(Comercio), igual al de comercio logeado. Asi se logra traer unicamente las fotos, de los 
			productos del comercio logeado.
		"""
		context['sinLeer']= Notificacion.objects.all().filter(destinatario = 'Comercio', id_destinatario = self.request.user.comercio.id, leido = False).count()
		#se retorna la variable de contexto
		return context
class Notificaciones(LoginRequiredMixin, TemplateView):

	login_url = 'principal:login'

	#Se indica el template a renderizar
	template_name = 'comercios/dashboard/notificaciones.html'
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(Notificaciones, self).get_context_data(**kwargs)
		context['notificaciones']= Notificacion.objects.all().filter(destinatario = 'Comercio', id_destinatario = self.request.user.comercio.id).order_by('-fecha_reg')
		#se retorna la variable de contexto
		return context
"""
	Clase VerComercio:
	Funcion que retorna los datos especificos de un comercio para mostrarlo estilo perfil

	variables:
		model
		template_name
		context_object_name
		context
		comercio

"""
class VerComercio(DetailView):

	model = Comercio
	template_name = 'comercios/comercio/ver_comercio.html'
	context_object_name = 'comercio'

	def get_context_data(self, **kwargs):
		context = super(VerComercio, self).get_context_data(**kwargs)
		comercio = context['comercio']
		context['compras'] = Compra.objects.all().filter(estado = 'recibido').count()
		context['productos'] = Producto.objects.all().filter(Comercio = comercio.id, activo=True)
		#al usar como parametro para filter("variable"__in = "lista") django recorre la lista de objetos dados
		#para devolver solo los que coincidan con la variable dada.
		context['fotos'] = Producto_Fotos.objects.all().filter(producto__in=context['productos'])
		context['publicaciones'] = Publicacion.objects.all().filter(comercio = comercio.id, activo=True)
		context['opiniones'] = Comercio_Opinion.objects.all().filter(comercio = comercio.id)
		try:
			context['seguido'] = YaSeguido(comercio, self.request.user.cliente)
			print(context['seguido'])
			if context['seguido'] and opino_comercio(request.user.cliente, comercio)==False:
				context['opinionForm'] = ComercioOpinionForm()
		except:
			pass
		return context
		


"""
	Clase ListaProductos:
	Se encarga de consulta unicamente productos con sus respectivas fotos del comercio logeado, para luego renderizarlos
	en el template asignado.

	variables:
		template_name
		context

"""
class ListaProductos(LoginRequiredMixin, TemplateView):
	login_url = 'principal:login' 
	#Se indica el template a renderizar
	template_name = 'comercios/productos/index.html'
	
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(ListaProductos, self).get_context_data(**kwargs)
		#se asigna a la variable de contexto todos los productos relacionados con el comercio logueado
		context['productos']=Producto.objects.all().filter(Comercio = self.request.user.comercio.id, activo = True)
		
		#se asigna a la variable de contexto todos las fotos relacionadas a los productos con el comercio logueado
		context['fotos'] = Producto_Fotos.objects.all().filter(producto__Comercio = self.request.user.comercio.id)
		
		
		#se retorna la variable de contexto
		return context

"""
	Funcion Add Producto:
	Funcion relacionada al caso de uso, Registrar producto.
	Se encarga de capturar la informacion de dos formularios, el formulario de fotografias para el producto, y el formulario del
	producto, relacionarlos a ambos, al producto con el comercio logeado y luego guardar.

	variables:
		productoF
		fotosF
		nuevoProducto
		comercio
		nuevoProducto
		fotosProducto
		productoForm
		fotoForm

"""
def AddProducto(request):

	if request.user.is_authenticated() == False:
		return redirect('principal:login')
	#Si la peticion realizada viene por POST se realiza en proceso de validacion y guardado
	if request.method == "POST":
		
		#Se asignan los datos recibidos a variables
		productoF = NuevoProductoForm(request.POST, prefix='producto')
		fotosF = ProductoFotosForm(request.POST, request.FILES, prefix='fotos')

		#Se validad y limpian los datos de ambos formularios
		if productoF.is_valid() and fotosF.is_valid():

			#Se guarda como objeto de tipo 'Producto' los datos del formulario a la variable 'nuevoProducto'
			nuevoProducto= productoF.save(commit=False)

			#Se crea un objeto de tipo 'Comercio' tomando como referencia el id del comercio logeado
			comercio = Comercio.objects.get(id = request.user.comercio.id)

			#se relaciona el objeto producto, con el objeto comercio
			nuevoProducto.Comercio = comercio

			#se guarda el nuevo producto en la BDD
			nuevoProducto.save()

			#Se crea un objeto de tipo 'Poducto_Fotos' con los datos del formulario
			fotosProducto = fotosF.save(commit=False)

			#Se relaciona el objeto de tipo 'Producto_Fotos'
			fotosProducto.producto = nuevoProducto	

			#Se guardan las fotos del Producto en la BDD
			fotosProducto.save()

			#Se guarda la realcion mucho a muchos relacionadas con el producto que estan en el formulario
			productoF.save_m2m()

			#se redirecciona al usuario
			return redirect('comerce_app:DashBoard')
		else:			
			context = {
				'fotoForm' : fotosF, 
				'productoForm' : productoF
			}
			return render(request, 'comercios/productos/nuevo.html', context)

	#Si la peticion no es post, o falla la validacion de los datos, se asignan los formularios
	#	como variables de contexto y se renderiza el template.
	productoForm = NuevoProductoForm(prefix='producto')
	fotoForm = ProductoFotosForm(prefix='fotos')
	context = {
		'fotoForm' : fotoForm, 
		'productoForm' : productoForm
	}
	return render(request, 'comercios/productos/nuevo.html', context)

"""
	Funcion 'EditarProducto':
	La funcion se encarga de buscar en la base de datos un producto, tomando como referencia el id recibido por parametro
	para devolverlos en un formulario cuando la peticion no sea de tipo 'POST'.

	Cuando la peticion es de tipo 'POST' valida y guarda la informacion.

	variables:
		producto
		foto
		productoF
		fotoF
"""
def EditarProducto(request, id):
	if request.user.is_authenticated() == False:
		return redirect('principal:login')
	#Se intenta obtener el Objeto de tipo producto de acuerdo al id y asignarlo a la variable, si no retorna un error 404
	producto = get_object_or_404(Producto, pk = id)

	#De obtener el producto, se obtiene de la BDD el objeto de tipo 'Producto_Fotos' de acuerdo al id del producto
	foto = Producto_Fotos.objects.get(producto = producto.id)

	#Si la peticion es de tipo 'POST' inicia el proceso de validacion y guardado
	if request.method == "POST":
		#Se asignan los datos recibidos del formulario a sus respectivas variables
		productoF = NuevoProductoForm(request.POST, prefix='producto', instance=producto)
		fotoF = ProductoFotosForm(request.POST, request.FILES, prefix='fotos', instance = foto)

		#Se valida y limpia la informacion de ambos formularios
		if productoF.is_valid() and fotoF.is_valid():
			
			#Se guardan ambos objetos en la BDD
			productoF.save()
			fotoF.save()

			#Se redirecciona al usuario.
			return redirect('comerce_app:DashBoard')
	
	#Si la peticion no es post, o falla la validacion de los datos, se asignan los formularios
	#	como variables de contexto y se renderiza el template.					
	productoF = NuevoProductoForm(prefix='producto', instance=producto)
	fotoF = ProductoFotosForm(prefix='fotos', instance = foto)
	context = {
		'fotoForm' : fotoF,
		'productoForm' : productoF,
		'fotos' : foto
	}
	return render(request, "comercios/productos/editar.html", context )

"""
	Clase 'EliminarProducto':
	Vista basada en clase encargada de la eliminarcion de un producto.
	Recibe el id del producto por la url, y muestra el producto, cuando la peticion es POST elimina el producto.

	NOTA: Al ser una vista basada en clases gran parte de esto ocurre 'tras vestidores'
"""

class  EliminarProducto(DetailView):
	#Se asigna el template a utilizar
	template_name = 'comercios/productos/eliminar.html'

	#se asigna el modelo a utilizar
	model = Producto

	#se asigna el nombre de la variable de contexto para el modelo Producto
	context_object_name = 'producto'

	def get_context_data(self, **kwargs):
		context = super(EliminarProducto, self).get_context_data(**kwargs)
		
		#se crea un objeto de tipo producto 
		producto = context['producto']
		
		#se obtienen las fotos correspondientes al producto de acuerdo al id del producto
		context['fotos']=Producto_Fotos.objects.get(producto = producto.id)
		context['preguntaForm'] = ProductoPreguntaForm(instance= Producto_Pregunta())
		context['respuestaForm'] = ProductoRespuestaForm(instance= Producto_Respuesta())
		context['preguntas'] = Producto_Pregunta.objects.all().filter(producto= producto.id)
		context['respuestas'] = Producto_Respuesta.objects.all().filter(producto = producto.id)
		context['opiniones'] = Producto_Opinion.objects.all().filter(producto = producto.id)
		#se retorna la variable de contexto
		return context

	def post(self, request, *args, **kwargs):		
		producto = self.get_object()
		producto.activo = False
		producto.save()
		return redirect ('comerce_app:VerProducto', pk=producto.id)

class  HabilitarProducto(DetailView):
	#Se asigna el template a utilizar
	template_name = 'comercios/productos/eliminar.html'

	#se asigna el modelo a utilizar
	model = Producto

	#se asigna el nombre de la variable de contexto para el modelo Producto
	context_object_name = 'producto'

	def get_context_data(self, **kwargs):
		context = super(HabilitarProducto, self).get_context_data(**kwargs)
		
		#se crea un objeto de tipo producto 
		producto = context['producto']
		
		#se obtienen las fotos correspondientes al producto de acuerdo al id del producto
		context['fotos']=Producto_Fotos.objects.get(producto = producto.id)
		context['preguntaForm'] = ProductoPreguntaForm(instance= Producto_Pregunta())
		context['respuestaForm'] = ProductoRespuestaForm(instance= Producto_Respuesta())
		context['preguntas'] = Producto_Pregunta.objects.all().filter(producto= producto.id)
		context['respuestas'] = Producto_Respuesta.objects.all().filter(producto = producto.id)
		context['opiniones'] = Producto_Opinion.objects.all().filter(producto = producto.id)
		#se retorna la variable de contexto
		return context

	def post(self, request, *args, **kwargs):		
		producto = self.get_object()
		producto.activo = True
		producto.save()
		return redirect ('comerce_app:VerProducto', pk=producto.id)

"""
	Clase 'VerProducto':
	Vista basada en clase que retorna los datos de un producto en especifico.
"""
class VerProducto(DetailView):
	#Se asigna el template a utilizar
	template_name = 'comercios/productos/ver.html'
	
	#se asigna el modelo a utilizar
	model = Producto
	
	#se asigna el nombre de la variable de contexto para el modelo Producto
	context_object_name = 'producto'
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(VerProducto, self).get_context_data(**kwargs)
		
		#se crea un objeto de tipo producto 
		producto = context['producto']
		
		#se obtienen las fotos correspondientes al producto de acuerdo al id del producto
		context['fotos']=Producto_Fotos.objects.get(producto = producto.id)
		context['preguntaForm'] = ProductoPreguntaForm(instance= Producto_Pregunta())
		context['respuestaForm'] = ProductoRespuestaForm(instance= Producto_Respuesta())
		context['preguntas'] = Producto_Pregunta.objects.all().filter(producto= producto.id)
		context['respuestas'] = Producto_Respuesta.objects.all().filter(producto = producto.id)
		context['opiniones'] = Producto_Opinion.objects.all().filter(producto = producto.id)
		print(opino(self.request.user.cliente, producto.id))
		print(compro(self.request.user.cliente, producto.id))
		try:
			if  not opino(self.request.user.cliente, producto.id) and compro(self.request.user.cliente, producto.id):
				context['ProductoopinionForm'] = ProductoOpinionForm()
		except:
			pass
		#se retorna la variable de contexto
		return context

"""
	Funcion 'PreguntarProducto':
	Vista basada en funcion que recibe como parametro el id del producto al cual se le relacionara la pregunta realizada por el cliente

"""

def PreguntarProducto(request, id):
	#Si la solicitud es POST comienza en proceso de validacion y guardado
	if request.method == "POST":
	
		#Se intenta obtener o objeto, de no existir se retorna un error 404
		producto = get_object_or_404(Producto, pk = id)

		#Se guardan en una variable los datos del formulario recibido
		preguntaF = ProductoPreguntaForm(request.POST)

		#Se valida y limpia la informacion del formulario
		if preguntaF.is_valid():
			
			#se crea un objeto de tipo Producto_Pregunta
			pregunta=preguntaF.save(commit=False)
			#se asocia la pregunta con el producto
			pregunta.producto = producto
			#se asocia la pregunta con usuario logeado de tipo cliente
			pregunta.cliente = request.user.cliente
			#Se guarda la prregunta en la BDD
			pregunta.save()
			#Se devuelve al usuario a la vista del producto
			enviar_notificacion(producto, 'pregunta', request.user.cliente, producto.Comercio)
			return redirect ('comerce_app:VerProducto', pk=id)

	#de no ser valido el formulario o no se POST la solicitud, se crea un formulario para ProductoPregunta
	preguntaF = ProductoPreguntaForm() 
	#y es enviado como contexto
	context = {
		'preguntaForm' : preguntaF
	}
	#a la vista del producto.
	return redirect ('comerce_app:VerProducto', pk=id)

"""
	Funcion 'ResponderProducto':
	Vista basada en funcion que recibe como parametro el id de la pregunta a la cual se le relacionara la respuesta realizada por el comercio
"""
def ResponderProducto(request, id, proID):
	#Si la solicitud es POST comienza en proceso de validacion y guardado
	if request.method == "POST":
	
		#Se intenta obtener o objeto, de no existir se retorna un error 404
		pregunta = get_object_or_404(Producto_Pregunta, pk = id)

		#Se guardan en una variable los datos del formulario recibido
		respuestaF = ProductoRespuestaForm(request.POST)
		print(respuestaF.errors)

		#Se valida y limpia la informacion del formulario
		if respuestaF.is_valid():
			#se crea un objeto de tipo Producto_Pregunta
			respuesta=respuestaF.save(commit=False)
			#se asocia la respuesta con la pregunta
			respuesta.pregunta = pregunta
			#se asocia la respuesta con el producto
			respuesta.producto = pregunta.producto
			#se asocia la respuesta con usuario logeado de tipo comercio
			respuesta.comercio = request.user.comercio
			#Se guarda la prregunta en la BDD
			respuesta.save()
			#Se devuelve al usuario a la vista del producto
			enviar_notificacion(pregunta.producto, 'respuesta', request.user.comercio, respuesta.pregunta.cliente)
			return redirect ('comerce_app:VerProducto', pk=proID)

	#de no ser valido se retorna a la vista del producto.
	return redirect ('comerce_app:VerProducto', pk=proID)


"""
	Clase 'ListaPublicaciones'
	Vista basada en clases que devuelve una lista con los respectivos comentarios de las publicaciones del comercio logeado
"""
class ListaPublicaciones(LoginRequiredMixin, TemplateView):
	login_url = 'principal:login'

	#Se asigna el template a utilizar
	template_name = 'comercios/publicaciones/index.html'
	
	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(ListaPublicaciones, self).get_context_data(**kwargs)		
		#Se obtienen las publicaciones del comercio logeado
		context['publicaciones']=Publicacion.objects.all().filter(comercio = self.request.user.comercio.id)		
		#Se obtienen los comentarios de las publicaciones del comercio logeado
		context['comentarios']=Publicacion_Comentario.objects.all().filter(publicacion__comercio = self.request.user.comercio.id)		
		#se retorna la variable de contexto
		return context

"""
	Clase 'AddPublicacion':
	Vista Basada en clase que guarda en la base de datos un objeto de tipo publicacion, relacionandolo con el comercio
	logeado.
"""
class AddPublicacion(LoginRequiredMixin, CreateView):
	login_url = 'principal:login'
	#se asigna el formulario a utilizar
	form_class= PublicacionForm

	#se asigna el template a utilizar
	template_name = 'comercios/publicaciones/nuevo.html'

	#se asigna el modelo a utilizar
	model = Publicacion

	#se asigna la url de exito
	success_url = reverse_lazy('comerce_app:ListarPublicaciones')

	#Funcion que se encarga de relacionar la publicacion con el comercio
	def form_valid(self, form):
		form.instance.comercio = self.request.user.comercio
		return super(AddPublicacion, self).form_valid(form)

"""
	Clase 'VerPublicacion:
	Vista basada en clase que se devuelve los datos especificos de una publicacion a un template
"""
class VerPublicacion(DetailView):

	#se asigna el template a utilizar
	template_name = 'comercios/publicaciones/ver.html'

	#se asigna el modelo a utilizar
	model = Publicacion

	#Se asigna el nombre de la variable de contexto
	context_object_name = 'publicacion'

	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(VerPublicacion, self).get_context_data(**kwargs)
		
		#se crea un objeto de tipo publicacion
		publicacion = context['publicacion']

		#Se asigna a la variable de contexto los comentarios relacionados con la publicacion
		context['comentarios']=Publicacion_Comentario.objects.all().filter(publicacion = publicacion.id)
		context['ComentarioForm']=PublicacionComentarioForm(instance=Publicacion_Comentario())
		# se retorna la variable de contexto.
		return context

"""
	clase 'EditarPublicacion':
	Vista basada en clase, que de acuerdo al id de una publicacion recibida por parameto muestra el formulario para la edicion
	y guarda los nuevos datos introducidos.
"""
class EditarPublicacion(LoginRequiredMixin, UpdateView):
	login_url = 'principal:login'
	#se asigna el formulario a utilizar
	form_class = PublicacionForm

	#se asigna la url de exito
	success_url = reverse_lazy('comerce_app:ListarPublicaciones')

	#se asigna el template a utilizar
	template_name = 'comercios/publicaciones/nuevo.html'

	#se asigna el modelo a utilizar
	model = Publicacion
	
"""
	clase 'EliminarPublicacion':
	Vista basada en funcion que inactiva una publicacion de acuerdo al id recibido por url de ser POST, si no, renderiza en el 
	template la publicacion a eliminar.
"""
class EliminarPublicacion(LoginRequiredMixin, DetailView):
	login_url = 'principal:login'
	#se asigna el template a utilizar
	template_name = 'comercios/publicaciones/eliminar.html'

	#se asigna el modelo a utilizar
	model = Publicacion
	
	#Se asigna el nombre a la variable de contexto a retornar
	context_object_name = 'publicacion'

	def post(self, request, *args, **kwargs):		
		publicacion = self.get_object()
		publicacion.activo = False
		publicacion.save()
		return redirect ('comerce_app:VerPublicacion', pk=publicacion.id)

class HabilitarPublicacion(LoginRequiredMixin, DetailView):
	login_url = 'principal:login'
	#se asigna el template a utilizar
	template_name = 'comercios/publicaciones/ver.html'

	#se asigna el modelo a utilizar
	model = Publicacion
	
	#Se asigna el nombre a la variable de contexto a retornar
	context_object_name = 'publicacion'

	def post(self, request, *args, **kwargs):		
		publicacion = self.get_object()
		publicacion.activo = True
		publicacion.save()
		return redirect ('comerce_app:VerPublicacion', pk=publicacion.id)

"""
	funcion 'ComentarPublicacion':
	Cuando la funcion recibe una solicitud de tipo POST, recibe y valida los datos recibidos, asociando el comentario a 
	la publicacion y guardando en la BDD
"""

def ComentarPublicacion(request, id):
	#Si la solicitud es POST comienza en proceso de validacion y guardado
	if request.method == "POST":
		#Se intenta obtener o objeto, de no existir se retorna un error 404
		publicacion = get_object_or_404(Publicacion, pk = id)

		#Se guardan en una variable los datos del formulario recibido
		comentarioF = PublicacionComentarioForm(request.POST)

		#Se valida y limpia la informacion del formulario
		if comentarioF.is_valid():
			#se crea un objeto de tipo Publicacion_Comentario
			comentario = comentarioF.save(commit=False)

			#se asocia el comentario con el usuario logeado
			comentario.usuario = request.user

			#se asocia el comentario con la publicacion
			comentario.publicacion = publicacion

			#Se guarda el comentario en la BDD
			comentario.save()
			enviar_notificacion(publicacion, 'comentario', request.user.cliente, publicacion.comercio)
			#Se devuelve al usuario a la vista de la publicacion
			return redirect('/comercios/ver_publicacion/%s/' %(id))
	#de no ser valido el formulario o no se POST la solicitud, se crea un formulario para PublicacionComentario
	comentarioF = PublicacionComentarioForm()

	#y es enviado como contexto
	context = {
		'PublicacionComentarioForm' : comentarioF
	}
	#a la vista de la publicacion.
	return redirect('/comercios/ver_publicacion/%s/' %(id))

def EliminarComentario(request, pk, pubID):
	comentario = get_object_or_404(Publicacion_Comentario, pk = pk, usuario = request.user.id)

	if request.method == "POST":
		comentario.delete()
		return redirect('comerce_app:VerPublicacion', pubID)
	return redirect('comerce_app:VerPublicacion', pubID)


"""
	Clase ListaVentas:
	Vista basada en clases que renderiza un template para mostrar las ventas realizadas por el comercio en sus distintos estados
"""
class ListaVentas(LoginRequiredMixin, TemplateView):
	login_url = 'principal:login'
	#Se asigna el template a renderizar
	template_name = 'comercios/dashboard/ventas.html'

	#Con la siguiente funcion se anexan variables de contexto adicionales a las ya creadas por la clase
	def get_context_data(self, **kwargs):
		context = super(ListaVentas, self).get_context_data(**kwargs)
		#se anexan las compras por procesar
		context['comprasProcesar'] = Compra.objects.all().filter(comercio = self.request.user.comercio.id, estado= 'en_proceso')
		#se anexan las compras por enviar
		context['comprasEnviar'] = Compra.objects.all().filter(comercio = self.request.user.comercio.id, estado= 'pagado')
		#se anexan las compras ya enviadas
		context['comprasEnviadas'] = Compra.objects.all().filter(comercio = self.request.user.comercio.id, estado= 'enviado')
		#se anexan las compras concretadas
		context['comprasListo'] = Compra.objects.all().filter(comercio = self.request.user.comercio.id, estado= 'recibido')

		return context
"""
	Clase VerVenta:
	Vista basada en clases que renderiza un template para mostrar una venta en especifico
"""
class VerVenta(LoginRequiredMixin, DetailView):
	login_url = 'principal:login'
	#se asigna el modelo a utilizar
	model = Compra
	#se asigna el template a a utilizar
	template_name = "comercios/dashboard/ver_venta.html"
	#se asigna nombre a la variable de contexto
	context_object_name = 'compra'
	def get_context_data(self, **kwargs): 
		context = super(VerVenta, self).get_context_data(**kwargs) 
		return context
"""
	funcion VerificarEnviar:
	Vista basada en funcion que cambia el estado de la compra recibida como argumento, verificando que la compra corresponda al comercio logeado. Luego retorna a la vista para ver la venta.
"""
def VerificarEnviar(request, pk):
	#se consulta en la BDD una compra que corresponda al id recbido como parametro y que corresponda al comercio que se encuentra logeado, de no tener exito retorna error 404
	compra = get_object_or_404(Compra, pk = pk, comercio = request.user.comercio.id)

	#si la peticion es POST
	if request.method == "POST":
		#se cambia es estado de la compra
		compra.estado = 'enviado'
		#se guarda el objeto
		compra.save()
		#se devuelve a la vista de ver venta, con la compra correspondiente
		enviar_notificacion(compra, 'enviado', compra.comercio, compra.cliente)
		return redirect('comerce_app:VerVenta', pk = compra.id)

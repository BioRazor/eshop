"""
	Plataforma comercial para la Promocion, Publicidad y Ventas de Productos en linea para las empresas del Municipio Juan German Roscio, Estado Guarico.
	Autor: David Abreu
"""
""" 
	DEFINICION:

	En esta seccion de codigo se realiza toda la logica de devolucion de respuesta de acuerdo a la URL recibida como peticion, ejecutando las clases o funciones asignadas a cada url,y enviado los argumentos dados de ser necesario.
"""
from django.conf.urls import patterns, url

#Se importan las vistas basadas en clases existentes en el archivo views.py
from .views import EditarProducto, ListaProductos, AddProducto, DashBoard, EliminarProducto, VerProducto, ListaPublicaciones, AddPublicacion, VerPublicacion, EditarPublicacion, EliminarPublicacion, ComentarPublicacion, PreguntarProducto, ResponderProducto, ListaVentas, VerVenta, VerificarEnviar, EliminarComentario, VerComercio, Notificaciones, HabilitarProducto, HabilitarPublicacion

urlpatterns = [
	#------------ COMERCIOS
	url(r'^dashboard/$', DashBoard.as_view(), name='DashBoard'),
	url(r'^ver_comercio/(?P<pk>\d+)/$', VerComercio.as_view(), name='VerComercio'),
	url(r'^notificaciones/$', Notificaciones.as_view(), name='VerNotificaciones'),
	#------------- PRODUCTOS-------------------
	url(r'^lista_productos/$', ListaProductos.as_view(), name='ListarProductos'),
	url(r'^ver_producto/(?P<pk>\d+)/$', VerProducto.as_view(), name='VerProducto'),
	url(r'^nuevo_producto/$', AddProducto, name='addProducto'),	
	url(r'^editar_producto/(?P<id>\d+)/$', EditarProducto, name='EditarProducto'),
	url(r'^eliminar_producto/(?P<pk>\d+)/$', EliminarProducto.as_view(), name='EliminarProducto'),
	url(r'^habilitar_producto/(?P<pk>\d+)/$', HabilitarProducto.as_view(), name='HabilitarProducto'),
	url(r'^preguntar/(?P<id>\d+)/$', PreguntarProducto, name='PreguntarProducto'),
	url(r'^responder/(?P<id>\d+)/(?P<proID>[0-9]+)$', ResponderProducto, name='ResponderProducto'),
	#-------------- PUBLICACIONES -------------------------
	url(r'^lista_publicaciones/$', ListaPublicaciones.as_view(), name='ListarPublicaciones'),
	url(r'^nueva_publicacion/$', AddPublicacion.as_view(), name='addPublicacion'),
	url(r'^ver_publicacion/(?P<pk>\d+)/$', VerPublicacion.as_view(), name='VerPublicacion'),
	url(r'^editar_publicacion/(?P<pk>\d+)/$', EditarPublicacion.as_view(), name='EditarPublicacion'),
	url(r'^eliminar_publicacion/(?P<pk>\d+)/$', EliminarPublicacion.as_view(), name='EliminarPublicacion'),
	url(r'^habilitar_publicacion/(?P<pk>\d+)/$', HabilitarPublicacion.as_view(), name='HabilitarPublicacion'),
	url(r'^comentar_publicacion/(?P<id>\d+)/$', ComentarPublicacion, name='ComentarPublicacion'),
	url(r'^eliminar_comentario/(?P<pk>\d+)/(?P<pubID>\d+)$', EliminarComentario, name='EliminarComentario'),
	#-------------VENTA DE PRODUCTOS (COMPRAS) --------------------------------
	url(r'^ventas/$', ListaVentas.as_view(), name='ListaVentas'),
	url(r'^ver_compra/(?P<pk>\d+)/$', VerVenta.as_view(), name='VerVenta'),
	url(r'^verificar_enviar/(?P<pk>\d+)/$', VerificarEnviar, name='VerificarEnviar'),
]

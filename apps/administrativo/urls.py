from django.conf.urls import patterns, url

from .views import IndexView, Login, Logout, RegistroComercio, RegistroCliente, Buscar, Productos, Publicaciones, ListarRecibos, VerRecibo, PagarRecibo, VerNotificacion, Comercios

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='home'),
	url(r'^login/$', Login, name='login'),
	url(r'^salir/$', Logout, name='salir'),
	url(r'^registro_comercio/$', RegistroComercio, name='RegistroComercio'),
	url(r'^registro_cliente/$', RegistroCliente, name='RegistroCliente'),
	url(r'^busqueda/$', Buscar, name='Buscar'),
	url(r'^productos/$', Productos.as_view(), name='Productos'),
	url(r'^publicaciones/$', Publicaciones.as_view(), name='Publicaciones'),
	url(r'^comercios/$', Comercios.as_view(), name='Comercios'),
	url(r'^ver_recibos/$', ListarRecibos.as_view(), name='ListarRecibos'),
	url(r'^ver_recibo/(?P<pk>\d+)/$', VerRecibo.as_view(), name='VerRecibo'),
	url(r'^pagar/(?P<pk>\d+)/$', PagarRecibo, name='PagarRecibo'),
	url(r'^ver_notificacion/(?P<pk>\d+)/$', VerNotificacion, name='VerNotificacion'),

]
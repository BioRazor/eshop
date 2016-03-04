from django.conf.urls import patterns, url

from .views import ComprarProducto, PagarProducto, DashBoard, SeguirComercio, ValorarProducto, RecibirProducto, ValorarComercio
urlpatterns = [
	url(r'^comprar/(?P<pk>\d+)/$', ComprarProducto, name='ComprarProducto'),
	url(r'^pagar/(?P<pk>\d+)/$', PagarProducto, name='PagarCompra'),
	url(r'^recibido/(?P<pk>\d+)/$', RecibirProducto, name='RecibirProducto'),
	url(r'^dashboard/$', DashBoard.as_view(), name='DashBoard'),
	url(r'^seguir_comercio/(?P<pkCli>\d+)/(?P<pkCo>\d+)$', SeguirComercio, name='SeguirComercio'),
	url(r'^valorar_producto/(?P<pkPro>\d+)/$', ValorarProducto, name='ValorarProducto'),
	url(r'^valorar_comercio/(?P<pkCo>\d+)/$', ValorarComercio, name='ValorarComercio'),
]
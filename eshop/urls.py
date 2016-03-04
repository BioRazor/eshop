"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

#Se importan las configuraciones del proyecto para verificar si esta en modo debug
from django.conf import settings



urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #Se incluyen las urls propias de cada aplicacion
    url(r'^', include('apps.administrativo.urls', namespace="principal")),
    url(r'^clientes/', include('apps.clientes.urls', namespace = "client_app")),
    url(r'^comercios/', include('apps.comercios.urls', namespace = "comerce_app")),

    
]

#funcion que permite mostrar las imagenes del proyecto cuando este se encuentra en modo DEBUG
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns("",
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,}
        ),
        url(r'^__debug__/', include(debug_toolbar.urls))
    )

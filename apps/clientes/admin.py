from django.contrib import admin

from .models import Cliente, Cliente_Seguir, Compra, Compra_Envio

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	search_fields = ('nombre', 'apellido', 'ci', 'direccion')
	list_display = ('nombre', 'apellido', 'ci', 'genero','activo')
	list_filter = ('genero', 'activo')
	filter_horizontal = ('area_interes',)

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
	pass

@admin.register(Compra_Envio)
class CompraEnvioAdmin(admin.ModelAdmin):
	pass

@admin.register(Cliente_Seguir)
class ClienteSeguirAdmin(admin.ModelAdmin):
	pass
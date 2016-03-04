from django.contrib import admin

from .models import Comercio, Producto, Producto_Fotos, Publicacion, Publicacion_Comentario, Comercio_Telefono, Producto_Opinion, Comercio_Opinion

class FotosInlines(admin.StackedInline):
	model = Producto_Fotos
	extra = 1

class ComentariosInlines(admin.StackedInline):
	model = Publicacion_Comentario

class TelefonoInlines(admin.StackedInline):
	model = Comercio_Telefono
	extra = 2

@admin.register(Comercio)
class ComercioAdmin(admin.ModelAdmin):
	list_filter=('activo', 'parroquia')
	inlines = [
		TelefonoInlines
	]

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_filter = ('activo', 'Comercio')
	list_display = ('nombre', 'id', 'Comercio', 'descripcion_corta', 'precio', 'stock', 'activo')
	search_fields= ('nombre', 'descripcion_corta', 'descripcion', 'comercio')
	filter_horizontal = ('area_interes',)
	inlines = [
		FotosInlines,
	]


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
	pass

@admin.register(Publicacion_Comentario)
class Publicacion_ComentarioAdmin(admin.ModelAdmin):
	pass

@admin.register(Producto_Opinion)
class ProductoOpinionAdmin(admin.ModelAdmin):
	pass
@admin.register(Comercio_Opinion)
class ComercioOpinionAdmin(admin.ModelAdmin):
	pass
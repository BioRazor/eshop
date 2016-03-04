from django.contrib import admin

from .models import Recibo, Agencia, Parroquia, Area_Interes, Usuario, Notificacion

@admin.register(Recibo)
class ReciboAdmin(admin.ModelAdmin):
	pass

@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
	pass

@admin.register(Parroquia)
class ParroquiaAdmin(admin.ModelAdmin):
	search_fields=('parroquia',)

@admin.register(Area_Interes)
class AreaInteresAdmin(admin.ModelAdmin):
	list_display = ('area_interes', 'gen_pref')
	list_filter = ('gen_pref',)
	search_fields = ('area_interes',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_filter = ('is_active', )
	search_fields = ('username', 'email')
	filter_horizontal = ('user_permissions',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
	pass
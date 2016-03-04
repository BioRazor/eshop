from django.db import models

class Cliente(models.Model):
	usuario = models.OneToOneField('administrativo.Usuario', blank=True, null=True)
	parroquia = models.OneToOneField('administrativo.Parroquia', blank=True, null=True)
	area_interes = models.ManyToManyField('administrativo.Area_Interes', blank=True)

	nombre = models.CharField(blank=False, max_length=50)
	apellido = models.CharField(blank=False, max_length=50)
	ci = models.CharField(blank=True, max_length=50)
	choices = (
		('M' , 'Masculino'),
		('F' , 'Femenino'),
		)
	genero = models.CharField(max_length=1, default='F', choices= choices)
	activo = models.BooleanField(default=True)
	direccion = models.TextField(blank=False)
	foto_perfil = models.ImageField(upload_to='clientes')

	class Meta:
		verbose_name='Cliente'
		verbose_name_plural='Clientes'

	def __str__(self):
		return ('%s %s') %(self.nombre, self.apellido)


class Cliente_Seguir(models.Model):
	cliente = models.ForeignKey(Cliente)
	comercio = models.ForeignKey('comercios.Comercio')

	class Meta:
		verbose_name='Seguido por Cliente'
		verbose_name_plural = 'Seguidos por Clientes'

	def __str__(self):
		return ('%s - %s') %(self.cliente, self.comercio)

class Compra_Envio(models.Model):
	agencia = models.ForeignKey('administrativo.Agencia')

	direccion = models.TextField(blank=False)
	detalles = models.TextField(default='Ninguno')
	fecha_recepcion = models.DateField(blank=True, null=True)

class Compra_Pago(models.Model):
	choices=(		
		('deposito', 'Deposito'),
		('trans', 'Transferencia'),
		)
	banco = models.CharField(blank=False, max_length=50, null=False)
	cuenta = models.PositiveSmallIntegerField(blank=False, null=False)
	nro_referencia = models.PositiveSmallIntegerField(blank=False, null=False) 
	tipo_pago = models.CharField(default='trans', max_length=50, choices=choices)
	fecha_pago = models.DateField(blank=True, null=True)
	

class Compra(models.Model):
	cliente = models.ForeignKey(Cliente)
	comercio = models.ForeignKey('comercios.Comercio')
	envio = models.OneToOneField(Compra_Envio, blank=True, null=True)
	pago = models.OneToOneField(Compra_Pago, blank=True, null=True)
	producto = models.ForeignKey('comercios.Producto')
	cantidad = models.PositiveSmallIntegerField(default=1)

	choices=(
		('en_proceso' , 'En Proceso'),
		('pagado' , 'Pagado'),
		('enviado' , 'Enviado'),
		('recibido' , 'Recibido'),
		)

	estado = models.CharField(default='en_proceso', max_length=50, choices= choices)
	fecha_compra = models.DateTimeField(auto_now_add=True)

	choices1 = (
		('personal', 'Entrega Personal'),
		('envio', 'Envio a Direccion'),
		)
	tipo_entrega = models.CharField(default='envio', max_length=50, choices= choices1)

	def __str__(self):
		return ('%s - %s - %s') %(self.cliente, self.comercio, self.producto)
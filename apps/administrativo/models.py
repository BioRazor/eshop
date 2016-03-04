#encoding:utf-8
from django.db import models

#imports necesarios para crear un Custom User Manager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


#Clase que hereda las funcionalidades y metodo necesario para la creacion de usuarios
class UserManager(BaseUserManager, models.Manager):

	#La siguiente funcion se encarga de crear el usuario en la base de datos, de acuerdo a los parametros recibidos
	def _create_user(self, username, email, password, is_staff,
				is_superuser, **extra_fields):

		#se normaliza y comprueba que se reciba un correro electronico
		email = self.normalize_email(email)
		if not email:
			raise ValueError('El email debe ser obligatorio')

		#Se crea un objeto con los datos recibidos por parametro
		user = self.model(username = username, email=email, is_active=True,
				is_staff = is_staff, is_superuser = is_superuser, **extra_fields)

		#Se realiza el proceso de hash del password o contraseña
		user.set_password(password)

		#Se garda el usuario en la base de datos utilizada actualmente
		user.save( using = self._db)

		#Se retorna el usuario creado
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password, False,
				False, **extra_fields)

	def create_superuser(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password, True,
				True, **extra_fields)

#Modelo Usuario, utilizado por el modelo Cliente, el modelo comercio.
#Tambien utilizado como Administrador o superusuario.
class Usuario(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(unique=True)

	#Se especifica el Manager para el modelo de usuario
	objects = UserManager()

	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)

	#Se especifica el campo a utilizar como Nombre de Usuario
	USERNAME_FIELD = 'username'
	#Se especifican los campos requeridos.
	REQUIRED_FIELDS = ['email']

	#Funcion que retorna el nombre de usuario, como nombre corto del objeto, al realizarse un llamado a este.
	def get_short_name(self):
		return self.username

class Recibo(models.Model):

	supervisor = models.ForeignKey(Usuario, blank=True, null=True)
	comercio = models.ForeignKey('comercios.Comercio')
	fecha_inicio = models.DateTimeField(auto_now_add=True)
	fecha_fin = models.DateTimeField(blank=True, null=True)
	activo = models.BooleanField(default=True)
	descripcion = models.TextField(blank=False)
	choices = (
		('por cancelar', 'En espera de Pago'),
		('por verificar pago', 'Es espera de verificación'),
		('pagado', 'Pagado'),
		('vencido', 'Vencido')
		)
	estado = models.CharField(choices=choices, max_length=50, default='por cancelar')

	class Meta:
		verbose_name='Factura'    
		verbose_name_plural='Facturas'

	def __str__(self):
		return '%s - %s' %(self.supervisor, self.comercio)

class PagoRecibo(models.Model):
	recibo = models.ForeignKey(Recibo)
	
	choices=(		
		('deposito', 'Deposito'),
		('transferencia', 'Transferencia'),
		)
	nro_referencia = models.PositiveSmallIntegerField(blank=False, null=False) 
	tipo_pago = models.CharField(default='transferencia', max_length=50, choices=choices)
	fecha_pago = models.DateField(blank=False, null=False)
	precio = models.PositiveSmallIntegerField(blank=False)

	class Meta:
		verbose_name='Pago de Recibo'    
		verbose_name_plural='Pago de Recibos'

	def __str__(self):
		return '%s - %s' %(self.recibo, self.fecha_pago)

class Agencia(models.Model):

	agencia = models.CharField(blank=False, max_length=50)
	descripcion = models.TextField(blank=False)
	foto_perfil = models.ImageField(upload_to='agencias')
	foto_portada = models.ImageField(upload_to='agencias')

	class Meta:
		verbose_name='Agencia'
		verbose_name_plural= 'Agencias'

	def __str__(self):
		return '%s' %(self.agencia)

class Parroquia(models.Model):

	parroquia = models.CharField(blank=False, max_length=50)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name='Parroquia'    
		verbose_name_plural='Parroquias'

	def __str__(self):
		return '%s' %(self.parroquia)

class Area_Interes(models.Model):

	area_interes = models.CharField(blank=False, max_length=50)
	choices = (
		('M', 'Masculino'),
		('F', 'Femenino'),
		('U', 'Unisex'),
		)
	gen_pref = models.CharField(max_length=50, choices = choices)

	class Meta:
		verbose_name='Area de Interes'    
		verbose_name_plural='Areas de Interes'

	def __str__(self):
		return '%s' %(self.area_interes)

class Notificacion(models.Model):
	modelo = models.CharField(blank=False, max_length=50)
	id_modelo = models.PositiveSmallIntegerField()
	fecha_reg = models.DateTimeField(auto_now_add=True)
	descripcion = models.TextField()
	relacionado = models.CharField(blank=False, max_length=50)
	id_relacionado = models.PositiveSmallIntegerField()
	leido = models.BooleanField(default=False)
	url = models.CharField(max_length=50)
	destinatario = models.CharField(blank=False, max_length=50)
	id_destinatario = models.PositiveSmallIntegerField()

	class Meta:
		verbose_name='Notificación'    
		verbose_name_plural='Notificaciones'

	def __str__(self):
		return '%s' %(self.descripcion)
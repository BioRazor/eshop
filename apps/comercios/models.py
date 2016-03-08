from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from ckeditor.fields import RichTextField

#Funcion que se encarga de validar que precio igresado sea mayor a cero
def validar_positivo(value):
	if value <0:
		raise ValidationError('Debe ingresar un precio mayor o igual a cero')

class Comercio(models.Model):
	parroquia = models.ForeignKey('administrativo.parroquia')
	usuario = models.OneToOneField('administrativo.usuario', blank=True, null=True)
	area_interes = models.ManyToManyField('administrativo.area_interes')

	nombre = models.CharField(blank=False, max_length=50)
	rif = models.CharField(blank=False, max_length=50)
	activo = models.BooleanField(default=True)
	direccion = models.TextField(blank=False)
	foto_perfil = models.ImageField(upload_to='comercios', blank=False)
	foto_portada = models.ImageField(upload_to='comercios', blank=False)
	slug = models.SlugField(max_length=100, editable=False)
	fecha_reg = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name='Comercio'    
		verbose_name_plural='Comercios'

	def __str__(self):
		return '%s' %(self.nombre)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Comercio, self).save(*args, **kwargs)

	def get_tlf(self):
		telefono = Comercio_Telefono.objects.get(pk = self.id)
		return ('%s-%s') %(telefono.prefijo, telefono.telefono)


class Comercio_Telefono(models.Model):
	comercio = models.ForeignKey(Comercio)

	choices=(
		('0246' , '0246'),
		('0412' , '0412'),
		('0416' , '0416'),
		('0426' , '0426'),
		('0424' , '0424'),
		('0414' , '0414'),

		)
	prefijo = models.CharField(choices=choices, max_length=4)
	telefono = models.PositiveIntegerField()

	def __str__(self):
		return ('%s-%s - %s') %(self.prefijo, self.telefono, self.comercio.nombre)
class Comercio_Opinion(models.Model):
	comercio = models.ForeignKey(Comercio)
	cliente = models.ForeignKey('clientes.Cliente')

	opinion = models.TextField(blank=False, max_length= 120)
	puntaje = models.PositiveSmallIntegerField(default=5)

	class Meta:
		verbose_name='Opinion sobre Comercio'
		verbose_name_plural='Opiniones sobre Comercios'

	def __str__(self):
		return ('%s - %s') %(self.comercio, self.cliente)

class Producto(models.Model):
	Comercio = models.ForeignKey(Comercio)
	area_interes = models.ManyToManyField('administrativo.area_interes')

	nombre = models.CharField(blank=False, max_length=50)
	descripcion = RichTextField(blank=False)
	descripcion_corta = models.TextField(max_length=140, blank=False)
	precio = models.DecimalField(max_digits=9, decimal_places=2, validators=[validar_positivo])
	stock = models.PositiveSmallIntegerField(blank=False)
	ancho = models.DecimalField(max_digits=6, decimal_places=2)
	largo = models.DecimalField(max_digits=6, decimal_places=2)
	alto = models.DecimalField(max_digits=6, decimal_places=2)
	peso = models.DecimalField(max_digits=6, decimal_places=2)
	visitas = models.PositiveSmallIntegerField(blank=True, default=0)
	activo = models.BooleanField(default=True)
	slug = models.SlugField(max_length=100, editable=False)

	class Meta:
		verbose_name='Producto'    
		verbose_name_plural='Productos'

	def __str__(self):
		return '%s' %(self.nombre)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Producto, self).save(*args, **kwargs)

	def get_pic(self):
		foto = Producto_Fotos.objects.get(pk = self.id)
		return foto.foto0.url


class Producto_Opinion(models.Model):
	producto = models.ForeignKey(Producto)
	cliente = models.ForeignKey('clientes.Cliente')

	opinion = models.TextField(blank=False, max_length= 120)
	puntaje = models.PositiveSmallIntegerField(default=5)

	class Meta:
		verbose_name='Opinion sobre Producto'
		verbose_name_plural='Opiniones sobre Productos'

	def __str__(self):
		return ('%s - %s') %(self.producto, self.cliente)

class Producto_Fotos(models.Model):
	producto = models.ForeignKey(Producto, blank=True)

	foto0 = models.ImageField(upload_to='productos', verbose_name='1ra Foto')
	foto1 = models.ImageField(upload_to='productos', verbose_name='2da Foto')
	foto2 = models.ImageField(upload_to='productos', verbose_name='3ra Foto')
	foto3 = models.ImageField(upload_to='productos', verbose_name='4ta Foto')

	def __str__(self):
		return ('>> %s') %(self.producto.nombre) 		

	class Meta:
		verbose_name='Fotos del Producto'
		verbose_name_plural='Fotos de Productos'

class Producto_Pregunta(models.Model):
	producto = models.ForeignKey(Producto)
	cliente = models.ForeignKey('clientes.Cliente')

	pregunta = models.TextField(blank=False)
	fecha = models.DateTimeField(auto_now_add=True)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return ('%s - %s') %(self.producto, self.cliente)

class Producto_Respuesta(models.Model):
	producto = models.ForeignKey(Producto)
	pregunta = models.ForeignKey(Producto_Pregunta)
	comercio = models.ForeignKey(Comercio)

	respuesta = models.TextField(blank=False)
	fecha = models.DateTimeField(auto_now_add=True)
	activo = models.BooleanField(default=True)

class Publicacion(models.Model):
	comercio = models.ForeignKey(Comercio)

	titulo = models.CharField(blank=False, max_length=50)
	contenido = RichTextField(blank=False)
	fecha_pub = models.DateTimeField(auto_now_add=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name='Publicacion'
		verbose_name_plural = 'Publicaciones'

	def __str__(self):
		return ('%s - %s') %(self.comercio, self.titulo)

	def count_comments(self):
		return Publicacion_Comentario.objects.all().filter(publicacion=self.id).count()

class Publicacion_Comentario(models.Model):
	usuario = models.ForeignKey('administrativo.usuario')
	publicacion = models.ForeignKey(Publicacion)

	comentario = models.TextField(blank=False)
	fecha_pub = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name='Comentario en Publicacion'
		verbose_name_plural = 'Comentarios en Publicaciones'

	def __str__(self):
		return ('%s - %s') %(self.cliente, self.publicacion)

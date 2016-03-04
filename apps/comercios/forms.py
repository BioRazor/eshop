from django import forms

#Se importan los modelos a utilizar
from .models import Producto, Producto_Fotos, Publicacion, Publicacion_Comentario, Producto_Pregunta, Producto_Respuesta, Producto_Opinion, Comercio_Opinion
#Se importa el Widget del editor de texto enriquecido
from ckeditor.widgets import CKEditorWidget


class NuevoProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		exclude = ('visitas', 'activo', 'Comercio')
		widgets= {
			'area_interes' : forms.CheckboxSelectMultiple(),
			'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
			'descripcion': forms.Textarea(),
			'descripcion_corta' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 3}),
			'precio' : forms.NumberInput(attrs={'min' : '1', 'class' : 'form-control'}),
			'stock' : forms.NumberInput(attrs={'min' : '1', 'class' : 'form-control'}),
			'ancho' : forms.NumberInput(attrs={'min' : '1', 'class' : 'form-control'}),
			'largo' : forms.NumberInput(attrs={'min' : '1', 'class' : 'form-control'}),
			'alto' : forms.NumberInput(attrs={'min' : '1', 'class' : 'form-control'}),
			'peso' : forms.NumberInput(attrs={'min' : '1', 'class' : 'form-control'}),
		}

class ProductoFotosForm(forms.ModelForm):
	class Meta:
		model = Producto_Fotos
		exclude = ('producto',)
		widgets = {
			'foto0' : forms.FileInput(),
			'foto1' : forms.FileInput(),
			'foto2' : forms.FileInput(),
			'foto3' : forms.FileInput(),
			'foto4' : forms.FileInput(),
		}

class PublicacionForm(forms.ModelForm):
	class Meta:
		model = Publicacion
		exclude = ('comercio', 'fecha_pub', 'activo')
		widgets = {
			'titulo' : forms.TextInput(attrs={'class' : 'form-control'}),
			'contenido' : forms.Textarea()

		}

class PublicacionComentarioForm(forms.ModelForm):
	class Meta:
		model = Publicacion_Comentario
		exclude = ('usuario', 'publicacion', 'fecha_pub')
		widgets = {
			'comentario' : forms.Textarea(attrs={'class' : 'form-control'}),
		}

class ProductoPreguntaForm(forms.ModelForm):
	class Meta:
		model = Producto_Pregunta
		exclude = ('producto', 'cliente', 'fecha')
		widgets = {
			'pregunta' : forms.Textarea(attrs={'class' : 'form-control'}),
		}

class ProductoRespuestaForm(forms.ModelForm):
	class Meta:
		model = Producto_Respuesta
		exclude = ('producto', 'fecha', 'comercio', 'pregunta')
		widgets = {
			'respuesta' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : '3', 'cols' : '4'}),
		}

class ProductoOpinionForm(forms.ModelForm):
	class Meta:
		model = Producto_Opinion
		exclude = ('producto', 'cliente', 'puntaje')
		widgets = {
			'opinion' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : '5', 'cols' : '4', 'required' : 'True'})
		}
class ComercioOpinionForm(forms.ModelForm):
	class Meta:
		model = Comercio_Opinion
		exclude = ('comercio', 'cliente', 'puntaje')
		widgets = {
			'opinion' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : '5', 'cols' : '4', 'required' : 'True'})
		}
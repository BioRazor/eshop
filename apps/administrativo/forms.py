#encoding:utf-8
from django import forms

from .models import Usuario, Recibo, PagoRecibo
from apps.comercios.models import Comercio, Comercio_Telefono
from apps.clientes.models import Cliente

class LoginForm(forms.Form):

	username = forms.CharField(max_length=30, 
				widget= forms.TextInput(attrs={
					'class' : 'form-control',
					'placeholder' : 'Ingresa tu Nombre de Usuario'
					}))
	password = forms.CharField(max_length=30, 
				widget= forms.TextInput(attrs={
					'type' : 'password',
					'class' : 'form-control',
					'placeholder' : 'Ingresa tu Contraseña'
					}))

class RegistroUsuarioForm(forms.ModelForm):
	passwordCheck = forms.CharField(max_length=30, widget=forms.PasswordInput(
																attrs={'class' : 'form-control',
																		'placeholder': 'Escribe de nuevo la contraseña',
																		'required' : 'True',
																		'type' : 'password',
																		'name' : 'passwordCheck'
																}))
	class Meta:
		model = Usuario
		fields = ('username', 'email', 'password')
		widgets = {
			'username' : forms.TextInput(attrs = 
				{
				'class' : 'form-control', 
				'placeholder' : 'Ingresa un nombre de usuario'
				}),
			'email' : forms.TextInput(attrs = 
				{
				'type' : 'email',
				'class' : 'form-control',
				'placeholder' : 'Ingresa un email'
				}),
			'password' : forms.TextInput(attrs = 
				{
				'type' : 'password',
				'class' : 'form-control',
				'placeholder' : 'Ingresa una contraseña',
				'required' : 'True',
				'name' : 'password',
				})
		}
	"""
	def clean_password(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordCheck')
		print (self.cleaned_data.get('passwordCheck'))
		print (password2)

		if not password2:
			self.add_error('passwordCheck', 'Debes escribir de nuevo la Contraseña')
		if password1 and password2 and password1 != password2:
			self.add_error('password' , 'Las contraseñas no coinciden')
		else:
			return self.cleaned_data['password']
	"""	
class RegistroComercioForm(forms.ModelForm):
	class Meta:
		model = Comercio
		exclude = ('usuario', 'activo', 'fecha_reg')
		widgets = {
			'nombre' : forms.TextInput(attrs={'class':'form-control'}),
			'rif' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Ej: J-12345678-9'}),			
			'direccion' : forms.Textarea(attrs={'class' : 'form-control'}),
			'foto_perfil' : forms.FileInput(),
			'foto_portada' : forms.FileInput(),
			'parroquia' : forms.Select(attrs={'class' : 'form-control'}),
			'area_interes' : forms.CheckboxSelectMultiple(),
		}
class ComercioTelefonoForm(forms.ModelForm):
	class Meta:
		model = Comercio_Telefono
		exclude = ('comercio',)
		widgets = {
			'prefijo' : forms.Select(attrs={'class':'form-control', 'placeholder' : '0246'}),
			'telefono' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234567'}),
		}

class RegistroClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente
		exclude = ('usuario', 'activo')
		widgets = {
			'nombre' : forms.TextInput(attrs={'class':'form-control'}),
			'apellido' : forms.TextInput(attrs={'class':'form-control'}),
			'ci' : forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'En Mayusculas, ejemplo: V-99999999'}),
			'genero' : forms.Select(attrs={'class' : 'form-control'}),
			'direccion' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Se usará para los envios a realizar'}),
			'foto_perfil' : forms.FileInput(),
			'parroquia' : forms.Select(attrs={'class' : 'form-control'}),
			'area_interes' : forms.CheckboxSelectMultiple()
		}

class PagoReciboForm(forms.ModelForm):
	meses = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'min' : 1, 'step' : 1, 'required' : 'True'}))
	class Meta:
		model = PagoRecibo
		exclude = ('recibo',)
		widgets= {
			'nro_referencia' : forms.TextInput(attrs={'class':'form-control', 'required' : 'True'}),
			'tipo_pago' : forms.Select(attrs={'class' : 'form-control'}),
			'fecha_pago' : forms.DateInput(attrs={'class' : 'form-control', 'type' : 'date'}),
			'precio' : forms.NumberInput(attrs={'class' : 'form-control', 'min' : 30000, 'step' : 30000, 'required' : 'True'}),
		}
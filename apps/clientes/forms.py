from django import forms

from .models import Compra, Compra_Envio, Compra_Pago

class CompraForm(forms.ModelForm):

	class Meta:
		model = Compra
		exclude = ('producto', 'comercio', 'cliente', 'envio', 'pago', 'estado')
		widgets = {
			'tipo_entrega' : forms.Select(attrs={'class' : 'form-control'}),
			'cantidad' : forms.NumberInput(attrs={'class' : 'form-control', 'min' : 1})
		}

class CompraEnvioForm(forms.ModelForm):

	class Meta:
		model = Compra_Envio
		fields = ['agencia', 'direccion', 'detalles', 'fecha_recepcion']
		widgets = {
			'agencia' : forms.Select(attrs={'class' : 'form-control'}),
			'direccion' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 3}),
			'detalles' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 3}),
			'fecha_recepcion' : forms.DateInput(attrs={'type' : 'date'})
		}

class CompraPagoForm(forms.ModelForm):

	class Meta:
		model= Compra_Pago
		fields = ['banco', 'cuenta', 'nro_referencia', 'tipo_pago', 'fecha_pago']
		widgets= {
			'banco' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Ej: Banco de Venezuela'}),
			'cuenta' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Ej: XXXXXXXXXXXXXXXXXX'}),
			'nro_referencia' : forms.TextInput(attrs={'class' : 'form-control'}),
			'tipo_pago' : forms.Select(attrs={'class' : 'form-control'}),
			'fecha_pago' : forms.TextInput(attrs={'type' : 'date', 'class' : 'form-control', 'placeholder' : 'Ej: 15/01/2016'})
		}

from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Layout, Submit
from django import forms

from sistema_monitoreo_app.choices import NIVELES_PELIGRO, PROCESOS
from sistema_monitoreo_app.models import Recomendacion, Error, Medicion, Variable, Regla, Proceso


# class ErrorForm(forms.Form):
#     variable = forms.CharField(label="Variable asociada")
#     nombre = forms.CharField(label="Nombre de error")
#     descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
#     peligro = forms.ChoiceField(choices=NIVELES_PELIGRO)
#
#     def clean(self):
#         # return all the clean data for the entire forms
#         all_clean_data = super().clean()
#         email = all_clean_data['email']
#         vmail = all_clean_data['verify_email']
#
#         if email != vmail:
#             raise forms.ValidationError("MAKE SURE EMAILS MATCH!")
#
#

class ErrorForm(forms.ModelForm):
    # descripcion = forms.CharField(widget=forms.Textarea)
    peligro = forms.ChoiceField(choices=NIVELES_PELIGRO)
    variable = forms.ModelMultipleChoiceField(Variable.objects.all(),
                                   widget=forms.CheckboxSelectMultiple, label="Variable afectada")
    es_error_de = forms.ChoiceField(choices=PROCESOS)

    class Meta:
        model = Error
        # fields = "__all__"
        exclude = ("medicion", "iri", "proceso")


class RecomendacionForm(forms.ModelForm):
    # descripcion = forms.CharField(widget=forms.Textarea)
    error = forms.ModelMultipleChoiceField(Error.objects.all(),
                                           widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Recomendacion
        # fields = "__all__"
        exclude = ("iri",)


class MedicionForm(forms.ModelForm):
    # Uni-form
    helper = FormHelper()

    class Meta:
        model = Medicion
        exclude = ("da_estado",
                   "mec_estado",
                   "fbr_estado",
                   "error",
                   "recomendacion",
                   "ml_label",)
        labels = {
            'da_dil1': _('Tasa de dilución'),
            'da_agv_in': _('AGV (entrada)'),
            'da_dqo_in': _('DQO (entrada)'),
            'da_biomasa_x': _('Biomasa'),
            'da_dqo_out': _('DQO (salida)'),
            'da_agv_out': _('AGV (Salida)'),
            'mec_agv_in': _('AGV (entrada)'),
            'mec_dil2': _('Tasa de dilución'),
            'mec_eapp': _('Eaap'),
            'mec_ace': _('AGV (salida)'),
            'mec_xa': _('xa'),
            'mec_xm': _('xm'),
            'mec_xh': _('xh'),
            'mec_mox': _('Mox'),
            'mec_imec': _('Imec'),
            'mec_qh2': _('QH2'),

        }
        help_texts = {
            'da_dil1': _('dil1 - e.g 0.6'),
            'da_agv_in': _('Concentración de acetato'),
            'da_dqo_in': _('Demanda Quimica de Oxígeno'),
            'da_biomasa_x': _('Biomasa'),
            'da_dqo_out': _('Demanda Quimica de Oxígeno'),
            'da_agv_out': _('Concentración de acetato'),
            'mec_agv_in': _('Concentración de acetato'),
            'mec_dil2': _('Tasa de dilución'),
            'mec_eapp': _('Voltaje aplicado a la MEC.'),
            'mec_ace': _('Concentración de acetato'),
            'mec_xa': _('Biomasa Anodofílicas'),
            'mec_xm': _('Biomasa Metanogénicas'),
            'mec_xh': _('Biomasa Hidrogenotropicas'),
            'mec_mox': _('Medidor de oxidación'),
            'mec_imec': _('Corriente eléctrica'),
            'mec_qh2': _('Flujo de Hidrógeno'),

        }


class ReglaForm(forms.ModelForm):
    class Meta:
        model = Regla
        exclude = ("storid",)

# class RecomendacionForm(forms.Form):
#     error = forms.ModelChoiceField(queryset=Error.objects.all())
#     nombre = forms.CharField(label="Nombre de error")
#     descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
#

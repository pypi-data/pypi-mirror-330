from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin, CrfSingletonModelFormMixin

from edc_he.form_validators import HealthEconomicsPatientFormValidator
from edc_he.forms import HealthEconomicsModelFormMixin

from ..models import HealthEconomicsPatient


class HealthEconomicsPatientForm(
    CrfSingletonModelFormMixin,
    HealthEconomicsModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsPatientFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        return super().clean()

    class Meta:
        model = HealthEconomicsPatient
        fields = "__all__"

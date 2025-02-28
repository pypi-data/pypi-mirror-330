from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin, CrfSingletonModelFormMixin

from edc_he.form_validators import HealthEconomicsPropertyFormValidator
from edc_he.forms import HealthEconomicsModelFormMixin

from ..models import HealthEconomicsProperty


class HealthEconomicsPropertyForm(
    CrfSingletonModelFormMixin,
    HealthEconomicsModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsPropertyFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        return super().clean()

    class Meta:
        model = HealthEconomicsProperty
        fields = "__all__"

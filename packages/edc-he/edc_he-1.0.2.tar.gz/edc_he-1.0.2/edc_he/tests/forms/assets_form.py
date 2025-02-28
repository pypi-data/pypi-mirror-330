from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin, CrfSingletonModelFormMixin

from edc_he.form_validators.assets_form_validator import (
    HealthEconomicsAssetsFormValidator,
)
from edc_he.forms import HealthEconomicsModelFormMixin

from ..models import HealthEconomicsAssets


class HealthEconomicsAssetsForm(
    CrfSingletonModelFormMixin,
    HealthEconomicsModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsAssetsFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        return super().clean()

    class Meta:
        model = HealthEconomicsAssets
        fields = "__all__"

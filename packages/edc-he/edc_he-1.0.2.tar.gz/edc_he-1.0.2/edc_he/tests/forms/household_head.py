from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_consent.utils import get_consent_model_cls
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin, CrfSingletonModelFormMixin
from edc_dx_review.form_mixins import ClinicalReviewBaselineRequiredModelFormMixin
from edc_utils import age

from edc_he.form_validators import HealthEconomicsHouseholdHeadFormValidator

from ..models import HealthEconomicsHouseholdHead


class HealthEconomicsHouseholdHeadForm(
    CrfSingletonModelFormMixin,
    ClinicalReviewBaselineRequiredModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsHouseholdHeadFormValidator

    def clean(self):
        cleaned_data = super().clean()
        self.clean_after_clean_fields_hoh_gender(cleaned_data)
        self.clean_after_clean_fields_hoh_age(cleaned_data)
        return cleaned_data

    def clean_after_clean_fields_hoh_gender(self, cleaned_data: dict):
        hoh = cleaned_data.get("hoh")
        hoh_gender = cleaned_data.get("hoh_gender")
        if hoh and hoh == YES and hoh_gender and hoh_gender != self.subject_consent.gender:
            raise forms.ValidationError(
                {
                    "hoh_gender": "Mismatch. Subject is the head of household and "
                    f"is {self.subject_consent.get_gender_display().lower()}."
                }
            )
        return hoh_gender

    def clean_after_clean_fields_hoh_age(self, cleaned_data: dict):
        hoh = cleaned_data.get("hoh")
        hoh_age = cleaned_data.get("hoh_age")
        if hoh and hoh == YES and hoh_age:
            if (
                hoh_age
                != age(self.subject_consent.dob, cleaned_data.get("report_datetime")).years
            ):
                age_in_years = age(
                    self.subject_consent.dob, cleaned_data.get("report_datetime")
                ).years
                raise forms.ValidationError(
                    {
                        "hoh_age": "Mismatch. Subject is the head of household and "
                        f"is {age_in_years} as of this report date."
                    }
                )
        return hoh_age

    @property
    def subject_consent(self):
        return get_consent_model_cls().objects.get(
            subject_identifier=self.get_subject_identifier()
        )

    class Meta:
        model = HealthEconomicsHouseholdHead
        fields = "__all__"
        help_texts = {
            "hoh_employment_type": format_html(
                "{}",
                mark_safe(
                    '<div class="form-row"><OL><LI><b>Chief executives, managers, senior '
                    "officials and legislators</b> </li>"
                    "<LI><b>Professionals, technicians and associate professionals</b>  (e.g. "
                    "science/engineering professionals, architects, nurses, doctors, "
                    "teachers, technicians, construction/mining supervisors, etc.)</li>"
                    "<LI><b>Clerks</b> (e.g. clerical support workers, receptionist, "
                    "secretary, postman/woman etc.) </li>"
                    "<LI><b>Service workers and shop sale workers</b> (e.g. shop sales, "
                    "cooks, waiter/bartenders, hairdressers, caretakers, street food/stall "
                    "salespersons, childcare workers, teachers aides, healthcare/personal "
                    "care assistants etc.) </li>"
                    "<LI><b>Large-scale agricultural, forestry and fishery workers</b> </li>"
                    "<LI><b>Subsistence farmers, fishers, etc.</b></li>"
                    "<LI><b>Craft and related workers</b> (e.g. builders, plumbers, painters, "
                    "mechanics, craftsmen, potters, welders, etc.) </li>"
                    "<LI><b>Plant and machine operators and assemblers, drivers</b> (e.g. "
                    "factory/plant operators, miners, truck/bus drivers, taxi drivers, "
                    "train drivers, etc.) </li>"
                    "<LI><b>Elementary occupations</b> (e.g. cleaners, farm pickers/"
                    "labourers, rickshaw drivers, builder assistants, hawkers, shoe shiners, "
                    "street car cleaners, garbage collectors, street sweepers, etc.) "
                    "</li></ol></div>"
                ),  # nosec B703, B308
            )
        }

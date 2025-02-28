from __future__ import annotations

from decimal import Decimal

from django import forms
from django.forms import ALL_FIELDS
from django.test import TestCase
from edc_constants.constants import FEMALE, MALE, NO, NOT_APPLICABLE, OTHER, YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import site_metadata_rules
from edc_metadata.tests.crf_test_helper import CrfTestHelper
from edc_utils import get_utcnow
from edc_utils.test_case_mixins.longitudinal_test_case_mixin import (
    LongitudinalTestCaseMixin,
)
from model_bakery.baker import make_recipe

from edc_he.calculators import InvalidAreaUnitsError
from edc_he.constants import ACRES, WIFE_HUSBAND
from edc_he.form_validators import HealthEconomicsHouseholdHeadFormValidator
from edc_he.models import (
    Education,
    EmploymentType,
    Ethnicities,
    InsuranceTypes,
    Religions,
)
from edc_he.rule_groups import HealthEconomicsRuleGroup as BaseHealthEconomicsRuleGroup
from edc_he.rule_groups import Predicates
from edc_he.utils import get_patient_model

from ..consents import consent_v1
from ..forms import HealthEconomicsAssetsForm as BaseHealthEconomicsAssetsForm
from ..forms import HealthEconomicsIncomeForm as BaseHealthEconomicsIncomeForm
from ..forms import HealthEconomicsPatientForm as BaseHealthEconomicsPatientForm
from ..forms import HealthEconomicsPropertyForm as BaseHealthEconomicsPropertyForm
from ..helper import Helper
from ..models import (
    HealthEconomicsAssets,
    HealthEconomicsHouseholdHead,
    HealthEconomicsPatient,
    HealthEconomicsProperty,
)
from ..visit_schedule import visit_schedule


def get_m2m_qs(model_cls, name: str = None):
    if name:
        qs = model_cls.objects.filter(name=name)
    else:
        name = model_cls.objects.all()[0].name
        qs = model_cls.objects.filter(name=name).exclude(name=NOT_APPLICABLE)
    return qs


def get_obj(model_cls, name: str = None):
    if name:
        obj = model_cls.objects.get(name=name)
    else:
        obj = model_cls.objects.all()[0]
    return obj


class HealthEconomicsPatientForm(BaseHealthEconomicsPatientForm):
    def validate_against_consent(self):
        pass


class HealthEconomicsAssetsForm(BaseHealthEconomicsAssetsForm):
    def validate_against_consent(self):
        pass


class HealthEconomicsPropertyForm(BaseHealthEconomicsPropertyForm):
    def validate_against_consent(self):
        pass


class HealthEconomicsIncomeForm(BaseHealthEconomicsIncomeForm):
    def validate_against_consent(self):
        pass


class HealthEconomicsTests(LongitudinalTestCaseMixin, CrfTestHelper, TestCase):
    consent_definition = consent_v1
    visit_schedule = visit_schedule
    helper_cls = Helper

    def setUp(self) -> None:
        self.subject_identifier = self.enroll()
        self.create_visits(self.subject_identifier)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        class HealthEconomicsRuleGroup(BaseHealthEconomicsRuleGroup):
            class Meta:
                app_label = "edc_he"
                source_model = "edc_visit_tracking.subjectvisit"
                predicates = Predicates()

        site_metadata_rules.register(HealthEconomicsRuleGroup)

    def get_cleaned_data(self, **kwargs) -> dict:
        """Cleaned data for HouseholdHead"""
        cleaned_data = dict(
            subject_visit=self.subject_visit_baseline,
            report_datetime=get_utcnow(),
            hh_count=5,
            hh_minors_count=1,
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
            relationship_to_hoh_other=None,
            hoh_gender=FEMALE,
            hoh_age=25,
            hoh_religion=get_obj(Religions),
            hoh_religion_other=None,
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_ethnicity_other=None,
            hoh_education=get_obj(Education),
            hoh_education_other=None,
            hoh_employment_status="",
            hoh_employment_type=get_obj(EmploymentType),
            hoh_employment_type_other=None,
            hoh_marital_status=OTHER,
            hoh_marital_status_other="blah",
            hoh_insurance=get_m2m_qs(InsuranceTypes),
            hoh_insurance_other=None,
        )
        cleaned_data.update(**kwargs)
        return cleaned_data

    def test_cleaned_data_ok(self):
        instance = HealthEconomicsHouseholdHead()
        cleaned_data = self.get_cleaned_data()
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data,
            instance=instance,
            model=HealthEconomicsHouseholdHead,
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_relationship_to_hoh_applicable_if_not_hoh(self):
        instance = HealthEconomicsHouseholdHead()
        opts = dict(
            instance=instance,
            model=HealthEconomicsHouseholdHead,
        )

        not_applicable_opts = dict(
            hoh_religion=get_obj(Religions, NOT_APPLICABLE),
            hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE),
            hoh_education=get_obj(Education, NOT_APPLICABLE),
            hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE),
            hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE),
        )
        cleaned_data = self.get_cleaned_data(hoh=YES, **not_applicable_opts)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_gender", form_validator._errors)
        self.assertIn(
            "This field is not applicable",
            str(form_validator._errors.get("hoh_gender")),
        )

        cleaned_data.update(hoh_gender=NOT_APPLICABLE, hoh=20)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_age", form_validator._errors)
        self.assertIn(
            "This field is not required",
            str(form_validator._errors.get("hoh_age")),
        )

        cleaned_data.update(hoh_age=0)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_age", form_validator._errors)
        self.assertIn(
            "This field is not required",
            str(form_validator._errors.get("hoh_age")),
        )

        cleaned_data.update(hoh_age=None, relationship_to_hoh=WIFE_HUSBAND)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh", form_validator._errors)
        self.assertIn(
            "This field is not applicable",
            str(form_validator._errors.get("relationship_to_hoh")),
        )

        cleaned_data.update(relationship_to_hoh=NOT_APPLICABLE)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_employment_status", form_validator._errors)
        self.assertIn(
            "This field is not applicable",
            str(form_validator._errors.get("hoh_employment_status")),
        )

        cleaned_data.update(
            hoh_employment_status=NOT_APPLICABLE, hoh_marital_status_other=None
        )
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_marital_status", form_validator._errors)
        self.assertIn(
            "This field is not applicable",
            str(form_validator._errors.get("hoh_marital_status")),
        )

        cleaned_data.update(hoh_marital_status=NOT_APPLICABLE)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        applicable_opts = dict(
            hoh_religion=get_obj(Religions),
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_education=get_obj(Education),
            hoh_employment_type=get_obj(EmploymentType),
            hoh_insurance=get_m2m_qs(InsuranceTypes),
        )

        cleaned_data.update(
            hoh=NO,
            hoh_gender=MALE,
            hoh_age=75,
            relationship_to_hoh=WIFE_HUSBAND,
            hoh_employment_status=NOT_APPLICABLE,
            **applicable_opts,
        )
        # hoh_employment_status
        cleaned_data.update(hoh_employment_status=NOT_APPLICABLE)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_employment_status", form_validator._errors)
        self.assertIn(
            "This field is applicable",
            str(form_validator._errors.get("hoh_employment_status")),
        )
        cleaned_data.update(hoh_employment_status="1")

        # hoh_marital_status
        cleaned_data.update(hoh_marital_status=NOT_APPLICABLE)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_marital_status", form_validator._errors)
        self.assertIn(
            "This field is applicable",
            str(form_validator._errors.get("hoh_marital_status")),
        )
        cleaned_data.update(hoh_marital_status="1")

        # ok
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        # check other specify
        cleaned_data.update(relationship_to_hoh=OTHER)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh_other", form_validator._errors)
        cleaned_data.update(relationship_to_hoh_other="blah")

        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_hoh_religion_other(self):
        instance = HealthEconomicsHouseholdHead()
        opts = dict(
            instance=instance,
            model=HealthEconomicsHouseholdHead,
        )
        applicable_opts = dict(
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_education=get_obj(Education),
            hoh_employment_type=get_obj(EmploymentType),
            hoh_insurance=get_m2m_qs(InsuranceTypes),
        )
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
            hoh_religion=None,
            **applicable_opts,
        )
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_religion", form_validator._errors)
        self.assertIn(
            "This field is applicable",
            str(form_validator._errors.get("hoh_religion")),
        )

        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
            hoh_religion=get_obj(Religions, OTHER),
            **applicable_opts,
        )
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_religion_other", form_validator._errors)
        self.assertIn(
            "This field is required",
            str(form_validator._errors.get("hoh_religion_other")),
        )

    def test_patient_required_if_patient_is_not_hoh(self):
        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        qs = self.crf_metadata_obj(get_patient_model(), NOT_REQUIRED, "1000")
        self.assertTrue(qs.exists())

        form = HealthEconomicsAssetsForm(data=cleaned_data)
        form.is_valid()
        self.assertIsNone(form._errors.get(ALL_FIELDS, None))

    def test_patient_required_if_patient_is_hoh(self):
        cleaned_data = self.get_cleaned_data(
            hoh=YES,
            relationship_to_hoh=NOT_APPLICABLE,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        qs = self.crf_metadata_obj(get_patient_model(), REQUIRED, "1000")
        self.assertTrue(qs.exists())

    def test_patient_required_before_assets_if_patient_is_hoh(self):
        cleaned_data = self.get_cleaned_data(
            hoh=YES,
            relationship_to_hoh=NOT_APPLICABLE,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        form = HealthEconomicsAssetsForm(data=cleaned_data)
        form.is_valid()
        msg = f"Complete {HealthEconomicsPatient._meta.verbose_name} CRF first"
        self.assertIn(msg, str(form._errors.get(ALL_FIELDS, "")))

    def test_patient_not_required_before_assets_if_patient_is_not_hoh(self):
        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        form = HealthEconomicsAssetsForm(data=cleaned_data)
        form.is_valid()
        msg = f"Complete {HealthEconomicsPatient._meta.verbose_name} CRF first"
        self.assertNotIn(msg, str(form._errors.get(ALL_FIELDS, "")))

    def test_assets_required_before_property_and_income(self):
        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        form = HealthEconomicsPropertyForm(data=cleaned_data)
        form.is_valid()
        msg = f"Complete {HealthEconomicsAssets._meta.verbose_name} CRF first"
        self.assertIn(msg, str(form._errors.get(ALL_FIELDS, "")))

        form = HealthEconomicsIncomeForm(data=cleaned_data)
        form.is_valid()
        self.assertIn(msg, str(form._errors.get(ALL_FIELDS, "")))

        make_recipe("edc_he.healtheconomicsassets", subject_visit=hoh_obj.subject_visit)

        form = HealthEconomicsPropertyForm(data=cleaned_data)
        form.is_valid()
        self.assertIsNone(form._errors.get(ALL_FIELDS, None))

        msg = f"Complete {HealthEconomicsProperty._meta.verbose_name} CRF first"
        form = HealthEconomicsIncomeForm(data=cleaned_data)
        form.is_valid()
        self.assertIn(msg, str(form._errors.get(ALL_FIELDS, "")))

    def test_property_required_before_income(self):
        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        make_recipe("edc_he.healtheconomicsassets", subject_visit=hoh_obj.subject_visit)

        msg = f"Complete {HealthEconomicsProperty._meta.verbose_name} CRF first"
        form = HealthEconomicsIncomeForm(data=cleaned_data)
        form.is_valid()
        self.assertIn(msg, str(form._errors.get(ALL_FIELDS, "")))

        make_recipe("edc_he.healtheconomicsproperty", subject_visit=hoh_obj.subject_visit)

        form = HealthEconomicsIncomeForm(data=cleaned_data)
        form.is_valid()
        self.assertIsNone(form._errors.get(ALL_FIELDS, None))

    def test_calculated_land_surface_area(self):
        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        make_recipe("edc_he.healtheconomicsassets", subject_visit=hoh_obj.subject_visit)

        obj = make_recipe(
            "edc_he.healtheconomicsproperty", subject_visit=hoh_obj.subject_visit
        )
        self.assertIsNone(obj.calculated_land_surface_area)

        obj.land_surface_area = 1
        obj.land_surface_area_units = None
        obj.save()
        self.assertIsNone(obj.calculated_land_surface_area)

        obj.land_surface_area = None
        obj.land_surface_area_units = ACRES
        obj.save()
        self.assertIsNone(obj.calculated_land_surface_area)

        obj.land_surface_area = 1
        obj.land_surface_area_units = "sq_xxx"
        with self.assertRaises(InvalidAreaUnitsError):
            obj.save()
        self.assertIsNone(obj.calculated_land_surface_area)

        obj.land_surface_area = 1
        obj.land_surface_area_units = ACRES
        obj.save()
        obj.refresh_from_db()
        self.assertEqual(obj.calculated_land_surface_area, Decimal("4046.86"))

        obj.land_surface_area = 1
        obj.land_surface_area_units = None
        obj.save()
        self.assertIsNone(obj.calculated_land_surface_area)

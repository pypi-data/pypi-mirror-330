from django.db import models
from django.utils.translation import gettext_lazy as _
from edc_crf.model_mixins import CrfModelMixin, SingletonCrfModelMixin
from edc_model.models import BaseUuidModel
from edc_visit_tracking.models import SubjectVisit

from edc_he.model_mixins import IncomeModelMixin


class HealthEconomicsIncome(
    SingletonCrfModelMixin,
    IncomeModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    subject_visit = models.OneToOneField(SubjectVisit, on_delete=models.PROTECT)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = _("Health Economics: Income")
        verbose_name_plural = _("Health Economics: Income")

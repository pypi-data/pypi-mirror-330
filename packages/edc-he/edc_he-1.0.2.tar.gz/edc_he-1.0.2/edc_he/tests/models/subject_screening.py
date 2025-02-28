from django.db import models
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow


class SubjectScreening(
    SiteModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    BaseUuidModel,
):
    screening_identifier = models.CharField(max_length=50)

    screening_datetime = models.DateTimeField(default=get_utcnow)

    report_datetime = models.DateTimeField(default=get_utcnow)

    age_in_years = models.IntegerField(default=25)

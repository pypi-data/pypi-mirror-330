from django.db import models
from django.db.models import PROTECT, Manager
from edc_constants.choices import GENDER_UNDETERMINED
from edc_constants.constants import FEMALE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_schedule.model_mixins import VisitScheduleModelMixin

from edc_consent.field_mixins import (
    CitizenFieldsMixin,
    IdentityFieldsMixin,
    PersonalFieldsMixin,
    ReviewFieldsMixin,
    VulnerabilityFieldsMixin,
)
from edc_consent.managers import ConsentObjectsByCdefManager, CurrentSiteByCdefManager
from edc_consent.model_mixins import (
    ConsentExtensionModelMixin,
    ConsentModelMixin,
    RequiresConsentFieldsModelMixin,
)


class SubjectScreening(SiteModelMixin, BaseUuidModel):

    screening_identifier = models.CharField(max_length=25, unique=True)

    initials = models.CharField(max_length=5, default="TO")

    age_in_years = models.IntegerField(default=25)

    gender = models.CharField(
        max_length=5,
        choices=GENDER_UNDETERMINED,
        default=FEMALE,
    )

    report_datetime = models.DateTimeField()

    eligible = models.BooleanField(default=False)

    eligibility_datetime = models.DateTimeField()

    objects = models.Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    class Meta:
        pass


class SubjectConsent(
    ConsentModelMixin,
    SiteModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    IdentityFieldsMixin,
    ReviewFieldsMixin,
    PersonalFieldsMixin,
    CitizenFieldsMixin,
    VulnerabilityFieldsMixin,
    BaseUuidModel,
):
    screening_identifier = models.CharField(
        verbose_name="Screening identifier", max_length=50, unique=True
    )
    history = HistoricalRecords()

    class Meta(ConsentModelMixin.Meta):
        pass


class SubjectConsentV1(SubjectConsent):
    on_site = CurrentSiteByCdefManager()
    objects = ConsentObjectsByCdefManager()

    class Meta:
        proxy = True


class SubjectConsentV1Ext(ConsentExtensionModelMixin, SiteModelMixin, BaseUuidModel):

    subject_consent = models.ForeignKey(SubjectConsentV1, on_delete=models.PROTECT)

    on_site = CurrentSiteManager()
    history = HistoricalRecords()
    objects = Manager()

    class Meta(ConsentExtensionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Subject Consent Extension V1.1"
        verbose_name_plural = "Subject Consent Extension V1.1"


class SubjectConsentUgV1(SubjectConsent):
    on_site = CurrentSiteByCdefManager()
    objects = ConsentObjectsByCdefManager()

    class Meta:
        proxy = True


class SubjectConsentV2(SubjectConsent):
    on_site = CurrentSiteByCdefManager()
    objects = ConsentObjectsByCdefManager()

    class Meta:
        proxy = True


class SubjectConsentV3(SubjectConsent):
    on_site = CurrentSiteByCdefManager()
    objects = ConsentObjectsByCdefManager()

    class Meta:
        proxy = True


class SubjectConsentV4(SubjectConsent):
    on_site = CurrentSiteByCdefManager()
    objects = ConsentObjectsByCdefManager()

    class Meta:
        proxy = True


class SubjectConsentUpdateToV3(SubjectConsent):
    class Meta:
        proxy = True


class SubjectReconsent(
    ConsentModelMixin,
    SiteModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    IdentityFieldsMixin,
    ReviewFieldsMixin,
    PersonalFieldsMixin,
    CitizenFieldsMixin,
    VulnerabilityFieldsMixin,
    BaseUuidModel,
):
    screening_identifier = models.CharField(
        verbose_name="Screening identifier", max_length=50, unique=True
    )
    history = HistoricalRecords()

    class Meta(ConsentModelMixin.Meta):
        pass


class SubjectConsent2(
    ConsentModelMixin,
    SiteModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    IdentityFieldsMixin,
    ReviewFieldsMixin,
    PersonalFieldsMixin,
    CitizenFieldsMixin,
    VulnerabilityFieldsMixin,
    BaseUuidModel,
):
    screening_identifier = models.CharField(
        verbose_name="Screening identifier", max_length=50, unique=True
    )

    history = HistoricalRecords()

    class Meta(ConsentModelMixin.Meta):
        pass


class SubjectVisit(
    SiteModelMixin, RequiresConsentFieldsModelMixin, VisitScheduleModelMixin, BaseUuidModel
):
    subject_identifier = models.CharField(max_length=25)
    report_datetime = models.DateTimeField(default=get_utcnow)

    # appointment = models.OneToOneField(Appointment, on_delete=CASCADE)
    # history = HistoricalRecords()
    pass


class TestModel(
    NonUniqueSubjectIdentifierModelMixin,
    RequiresConsentFieldsModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    report_datetime = models.DateTimeField(default=get_utcnow)


class CrfOne(
    RequiresConsentFieldsModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    @property
    def related_visit(self):
        return self.subject_visit

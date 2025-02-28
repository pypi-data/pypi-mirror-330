from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from edc_utils import get_utcnow

from edc_facility.form_validators import HealthFacilityFormValidator
from edc_facility.forms import HealthFacilityForm
from edc_facility.models import HealthFacility, HealthFacilityTypes


class TestForm(TestCase):
    def test_form_validator_ok(self):
        form_validator = HealthFacilityFormValidator(
            cleaned_data=dict(tue=True, thu=True),
            instance=HealthFacility,
        )
        form_validator.validate()
        self.assertEqual(form_validator._errors, {})

    def test_form_ok(self):
        data = dict()

        form = HealthFacilityForm(data=data, instance=HealthFacility())
        form.is_valid()
        self.assertIn("report_datetime", form._errors)

        data = dict(
            report_datetime=get_utcnow(),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        form = HealthFacilityForm(data=data, instance=HealthFacility())
        form.is_valid()
        self.assertIn("name", form._errors)

        data = dict(
            report_datetime=get_utcnow(),
            name="My Health Facility",
            site=Site.objects.get(id=settings.SITE_ID),
        )
        form = HealthFacilityForm(data=data, instance=HealthFacility())
        form.is_valid()
        self.assertIn("health_facility_type", form._errors)

        data = dict(
            report_datetime=get_utcnow(),
            name="My Health Facility",
            health_facility_type=HealthFacilityTypes.objects.all()[0],
            site=Site.objects.get(id=settings.SITE_ID),
        )
        form = HealthFacilityForm(data=data, instance=HealthFacility())
        form.is_valid()
        self.assertIn("__all__", form._errors)
        self.assertIn("Select at least one clinic day", str(form._errors))

        data = dict(
            report_datetime=get_utcnow(),
            name="My Health Facility",
            health_facility_type=HealthFacilityTypes.objects.all()[0],
            tue=True,
            thu=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        form = HealthFacilityForm(data=data, instance=HealthFacility())
        form.is_valid()
        self.assertEqual({}, form._errors)

        form.save()

        try:
            HealthFacility.objects.get(name="MY HEALTH FACILITY")
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised")

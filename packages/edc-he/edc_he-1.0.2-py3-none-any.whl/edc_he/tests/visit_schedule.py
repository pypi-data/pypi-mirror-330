from dateutil.relativedelta import relativedelta
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf, CrfCollection, Visit
from edc_visit_schedule.visit_schedule import VisitSchedule

from edc_he.tests.consents import consent_v1
from edc_he.utils import (
    get_assets_model,
    get_household_head_model,
    get_income_model,
    get_patient_model,
    get_property_model,
)

crfs = CrfCollection(
    Crf(show_order=10, model=get_household_head_model(), required=True),
    Crf(show_order=20, model=get_patient_model(), required=True),
    Crf(show_order=30, model=get_assets_model(), required=True),
    Crf(show_order=40, model=get_income_model(), required=True),
    Crf(show_order=50, model=get_property_model(), required=True),
)

visit0 = Visit(
    code="1000",
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
)

visit1 = Visit(
    code="2000",
    title="Day 2",
    timepoint=1,
    rbase=relativedelta(days=1),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
)

visit2 = Visit(
    code="3000",
    title="Day 3",
    timepoint=2,
    rbase=relativedelta(days=2),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
)

visit3 = Visit(
    code="4000",
    title="Day 4",
    timepoint=3,
    rbase=relativedelta(days=3),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
)

schedule = Schedule(
    name="schedule",
    onschedule_model="visit_schedule_app.onschedule",
    offschedule_model="visit_schedule_app.offschedule",
    appointment_model="edc_appointment.appointment",
    consent_definitions=[consent_v1],
)

schedule.add_visit(visit0)
schedule.add_visit(visit1)
schedule.add_visit(visit2)
schedule.add_visit(visit3)

visit_schedule = VisitSchedule(
    name="visit_schedule",
    offstudy_model="visit_schedule_app.subjectoffstudy",
    death_report_model="visit_schedule_app.deathreport",
)

visit_schedule.add_schedule(schedule)

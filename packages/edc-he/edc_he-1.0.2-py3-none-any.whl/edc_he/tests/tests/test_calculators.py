from decimal import Decimal

from django.test import TestCase

from edc_he.calculators import (
    InvalidAreaUnitsError,
    acres_to_sq_meters,
    convert_to_sq_meters,
    decimals_to_sq_meters,
    hectares_to_sq_meters,
    sq_feet_to_sq_meters,
)
from edc_he.constants import ACRES, DECIMALS, HECTARES, SQ_FEET, SQ_METERS


class TestCalculators(TestCase):
    def test_acres_to_sq_metres(self):
        for area, expected_output in [
            (1, Decimal("4046.8564224")),
            (2, Decimal("8093.7128448")),
            (10, Decimal("40468.564224")),
        ]:
            with self.subTest(area=area, expected_output=expected_output):
                self.assertEqual(acres_to_sq_meters(area), expected_output)

    def test_decimals_to_sq_metres(self):
        for area, expected_output in [
            (1, Decimal("40.468564224")),
            (2, Decimal("80.937128448")),
            (5, Decimal("202.34282112")),
            (10, Decimal("404.68564224")),
            (12.5, Decimal("505.8570528")),
            (20, Decimal("809.37128448")),
            (50, Decimal("2023.4282112")),
            (99, Decimal("4006.387858176")),
            (100, Decimal("4046.8564224")),
        ]:
            with self.subTest(area=area, expected_output=expected_output):
                self.assertEqual(decimals_to_sq_meters(area), expected_output)

    def test_hectares_to_sq_metres(self):
        for area, expected_output in [
            (1, Decimal("10_000")),
            (2, Decimal("20_000")),
            (5, Decimal("50_000")),
            (10, Decimal("100_000")),
        ]:
            with self.subTest(area=area, expected_output=expected_output):
                self.assertEqual(hectares_to_sq_meters(area), expected_output)

    def test_sq_feet_to_sq_metres(self):
        for area, expected_output in [
            (50 * 50, Decimal("232.2576")),
            (100 * 100, Decimal("929.0304")),
            (100 * 50, Decimal("464.5152")),
        ]:
            with self.subTest(area=area, expected_output=expected_output):
                self.assertEqual(sq_feet_to_sq_meters(area), expected_output)

    def test_equivalent_conversions(self):
        # 1 hectare == 10,000 square meters
        self.assertEqual(hectares_to_sq_meters(1), 10_000)

        # 1 hectare ~= 2.47 acres (within 5 square meters)
        self.assertAlmostEqual(hectares_to_sq_meters(1), acres_to_sq_meters(2.47), delta=5)

        # 259 hectares ~= 640 acres (within 12 square meters)
        self.assertAlmostEqual(hectares_to_sq_meters(259), acres_to_sq_meters(640), delta=12)

        # 1 acre ~= 4046.86 square meters (within 1 square cm)
        self.assertAlmostEqual(acres_to_sq_meters(1), Decimal(4046.86), delta=0.01)

        # 1 acre == 43,560 square feet
        self.assertEqual(acres_to_sq_meters(1), sq_feet_to_sq_meters(43_560))

        # 1 acre == 100 decimals
        self.assertEqual(acres_to_sq_meters(1), decimals_to_sq_meters(100))

        # 50 decimals == half an acre
        self.assertEqual(decimals_to_sq_meters(50), acres_to_sq_meters(1) / 2)
        self.assertEqual(decimals_to_sq_meters(50), acres_to_sq_meters(0.5))

        # 25 decimals == quarter an acre
        self.assertEqual(decimals_to_sq_meters(25), acres_to_sq_meters(1) / 4)
        self.assertEqual(decimals_to_sq_meters(25), acres_to_sq_meters(0.25))

        # 12.5 decimals == eighth an acre
        self.assertEqual(decimals_to_sq_meters(12.5), acres_to_sq_meters(1) / 8)
        self.assertEqual(decimals_to_sq_meters(12.5), acres_to_sq_meters(0.125))

        # 1 square meter ~= 10.7 square feet
        self.assertAlmostEqual(Decimal("1"), sq_feet_to_sq_meters(10.7639), delta=0.001)

        # 1 foot == 0.348 meters
        # 1 square foot == 0.3048 * 0.3048 square meters
        self.assertEqual(sq_feet_to_sq_meters(1), Decimal("0.3048") * Decimal("0.3048"))

    def test_convert_to_sq_meters(self):
        self.assertEqual(convert_to_sq_meters(area=123, area_units=SQ_METERS), Decimal("123"))

        self.assertEqual(
            convert_to_sq_meters(area=1, area_units=ACRES),
            Decimal("4046.8564224"),
        )

        self.assertEqual(
            convert_to_sq_meters(area=100, area_units=DECIMALS),
            Decimal("4046.8564224"),
        )

        self.assertEqual(convert_to_sq_meters(area=1, area_units=HECTARES), Decimal("10_000"))

        self.assertEqual(
            convert_to_sq_meters(area=200 * 200, area_units=SQ_FEET), Decimal("3716.1216")
        )

    def test_convert_to_sq_meters_unrecognised_units_raises(self):
        with self.assertRaises(InvalidAreaUnitsError):
            convert_to_sq_meters(area=2, area_units="unsupported_units")

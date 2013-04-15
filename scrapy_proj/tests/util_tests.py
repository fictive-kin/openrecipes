from openrecipes.util import get_isodate, parse_isodate, get_isoduration, parse_isoduration
import unittest
import datetime


class ISODateTests(unittest.TestCase):

    def test_get_isodate(self):
        self.assertEqual('2009-10-11', get_isodate("October 11 2009"))

    def test_parse_isodate(self):
        dt = datetime.date(year=2009, month=10, day=11)
        self.assertEqual(dt, parse_isodate('2009-10-11'))

    def test_get_isoduration(self):
        self.assertEqual('PT15M', get_isoduration("15 minutes"))

    def test_parse_isoduration(self):
        delta = datetime.timedelta(days=1)
        self.assertEqual(delta, parse_isoduration('P1D'))

    def test_parse_isoduration_2(self):
        delta = datetime.timedelta(minutes=15)
        self.assertEqual(delta, parse_isoduration('PT15M'))

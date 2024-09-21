from django.test import TestCase
from datetime import datetime
from .api import parse_date, parse_review_id_from_api_name

class DateTimeParseTests(TestCase):
    def test_parse_from_api(self):
        datetime_from_api="2024-09-13T10:03:08Z"
        parsed_datetime = parse_date(datetime_from_api)
        correct_datetime = datetime(2024, 9, 13, 10, 3, 8)
        self.assertEqual(correct_datetime, parsed_datetime)

class ReviewIDParseTests(TestCase):
    def test_parse_review_id_from_api_name(self):
        name_from_api="places/ChIJJ2iPNY27EmsR45MJL04zqTc/reviews/ChdDSUhNMG9nS0VJQ0FnSURIck1TYjJnRRAB"
        parsed_id = parse_review_id_from_api_name(name_from_api)
        correct_id = "ChdDSUhNMG9nS0VJQ0FnSURIck1TYjJnRRAB"
        self.assertEqual(parsed_id, correct_id)
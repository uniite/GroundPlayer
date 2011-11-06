"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from tasks import ScanMediaTask


class ScanMediaTest(TestCase):
    def test_scan_media(self):
        ScanMediaTask().run(r"U:\Music\Pendulum", False)


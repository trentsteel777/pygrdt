from django.test import TestCase
from analysisportal.models import Watchlist


# Create your tests here.

class AnimalTestCase(TestCase):
    def setUp(self):
        Watchlist.objects.create(name="cat")

    def test_animals_can_speak(self):
        cat = Watchlist.objects.get(name="cat")
        self.assertEqual(cat.name, "cat")
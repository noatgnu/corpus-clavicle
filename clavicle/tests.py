from django.test import TestCase
from clavicle.models import DifferentialAnalysis, RawData
# Create your tests here.


class DifferentialAnalysisTestCase(TestCase):
    databases = {'clavicle'}

    def setUp(self) -> None:
        DifferentialAnalysis.objects.create()

    def test_differential_analysis(self):
        c = DifferentialAnalysis.objects.all()
        assert c[c.count()-1].name == "test"
        assert c[c.count()-1].description == "test"


class RawDataTestCase(TestCase):
    databases = {'clavicle'}

    def setUp(self) -> None:
        RawData.objects.create()

    def test_raw_data(self):
        c = RawData.objects.all()
        assert c[c.count()-1].name == "test"
        assert c[c.count()-1].description == "test"

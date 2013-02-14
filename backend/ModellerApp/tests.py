"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


def jsonTestSetup():
  from ModellerApp.utils import GlassConfig
  from ModellerApp.models import BasicLensData
  from django.contrib.auth.models import User
  
  st = '{"__type":"model","NrOf":{"__type":"counters","Sources":1,"ExtremalPoints":5,"Contours":4,"ContourPoints":12},"Sources":[{"__type":"extpnt","idnr":0,"x":267,"y":189,"depth":0,"isRoot":true,"isExpanded":true,"childrenInsideEachOther":false,"type":"sad","wasType":"min","child1":{"__type":"extpnt","idnr":1,"x":390,"y":254,"depth":1,"isRoot":false,"isExpanded":true,"childrenInsideEachOther":true,"type":"sad","wasType":"min","child1":{"__type":"extpnt","idnr":3,"x":362,"y":234,"depth":2,"isRoot":false,"isExpanded":false,"childrenInsideEachOther":false,"type":"max","wasType":"","child1":null,"child2":null,"contour":{"__type":"contour","idnr":2,"cpoints":[{"__type":"cpnt","idnr":6,"r_fac":0.625,"d_phi":1.5708},{"__type":"cpnt","idnr":7,"r_fac":0.5,"d_phi":3.1416},{"__type":"cpnt","idnr":8,"r_fac":0.625,"d_phi":4.7124}]}},"child2":{"__type":"extpnt","idnr":4,"x":337,"y":212,"depth":2,"isRoot":false,"isExpanded":false,"childrenInsideEachOther":false,"type":"min","wasType":"","child1":null,"child2":null,"contour":{"__type":"contour","idnr":3,"cpoints":[{"__type":"cpnt","idnr":9,"r_fac":0.625,"d_phi":1.5708},{"__type":"cpnt","idnr":10,"r_fac":0.5,"d_phi":3.1416},{"__type":"cpnt","idnr":11,"r_fac":0.625,"d_phi":4.7124}]}},"contour":{"__type":"contour","idnr":0,"cpoints":[{"__type":"cpnt","idnr":0,"r_fac":0.625,"d_phi":1.5708},{"__type":"cpnt","idnr":1,"r_fac":0.5,"d_phi":3.1416},{"__type":"cpnt","idnr":2,"r_fac":0.625,"d_phi":4.7124}]}},"child2":{"__type":"extpnt","idnr":2,"x":215,"y":144,"depth":1,"isRoot":false,"isExpanded":false,"childrenInsideEachOther":false,"type":"min","wasType":"","child1":null,"child2":null,"contour":{"__type":"contour","idnr":1,"cpoints":[{"__type":"cpnt","idnr":3,"r_fac":0.625,"d_phi":1.5708},{"__type":"cpnt","idnr":4,"r_fac":0.5,"d_phi":3.1416},{"__type":"cpnt","idnr":5,"r_fac":0.625,"d_phi":4.7124}]}},"contour":null}],"ExternalMasses":[{"__type":"ext_mass","idnr":0,"x":130,"y":276,"r":30,"phi":0.7853981633974483}],"Rulers":[{"__type":"ruler","idnr":0,"x":312,"y":94,"r":30,"phi":0.7853981633974483}],"MinMmaxSwitchAngle":1.0471975511965976}'
  bld = BasicLensData.objects.all()[0]
  u = User.objects.all()[0]
  gc = GlassConfig(u, bld)
  
  return (st, bld, u, gc)
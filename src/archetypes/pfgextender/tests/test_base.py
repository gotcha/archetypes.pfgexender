import unittest

from Products.PloneTestCase import PloneTestCase

from archetypes.pfgextender.testing import layer
from archetypes.pfgextender.tests import IBirth

PloneTestCase.setupPloneSite()


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testInstalled(self):
        self.failUnless(
            hasattr(self.portal, 'formgen_tool'))

    def testFactory(self):
        id = self.folder.invokeFactory('Birth', 'birth')
        birth = getattr(self.folder, id)
        self.failUnless(IBirth.providedBy(birth))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite

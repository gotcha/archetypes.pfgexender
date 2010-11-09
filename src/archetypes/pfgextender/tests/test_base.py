import unittest


from Products.PloneTestCase import PloneTestCase

from archetypes.pfgextender.testing import layer

PloneTestCase.setupPloneSite()


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testInstalled(self):
        self.failUnless(
            hasattr(self.portal, 'formgen_tool'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite

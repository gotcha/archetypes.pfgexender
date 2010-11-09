import unittest


from Products.PloneTestCase import PloneTestCase

from archetypes.pfgextender.testing import layer

PloneTestCase.setupPloneSite()


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testDummy(self):
        self.failUnless(self.portal.pfg)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite

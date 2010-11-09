import unittest

from zope.component import provideUtility

from Products.PloneTestCase import PloneTestCase
from Products.PloneFormGen.interfaces import IPloneFormGenForm

from archetypes.pfgextender.testing import layer
from archetypes.pfgextender.testing import populate
from archetypes.pfgextender.testing import FORM_ID
from archetypes.pfgextender.testing import TEXT_ID
from archetypes.pfgextender.tests import IBirth

PloneTestCase.setupPloneSite()

DOCUMENT_ID = 'document'


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testInstalled(self):
        self.failUnless(
            hasattr(self.portal, 'formgen_tool'))

    def testFactory(self):
        id = self.folder.invokeFactory('Birth', 'birth')
        birth = getattr(self.folder, id)
        self.failUnless(IBirth.providedBy(birth))

    def testPopulated(self):
        populate(self.folder)
        self.failUnless(FORM_ID in self.folder)

    def testTypeIsExtended(self):
        populate(self.folder)
        pfgForm = getattr(self.folder, FORM_ID)
        provideUtility(pfgForm, provides=IPloneFormGenForm)
        self.folder.invokeFactory('Document', DOCUMENT_ID)
        document = getattr(self.folder, DOCUMENT_ID)
        schema = document.Schema()
        self.failUnless(TEXT_ID in schema.keys())
        field = schema.getField(TEXT_ID)
        self.assertEquals(field.getName(), TEXT_ID)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite

import unittest
import transaction

from zope.component import queryUtility

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.tools.formGenTool import FormGenTool

from archetypes.pfgextender.tool import TOOL_ID
from archetypes.pfgextender.interfaces import IPFGExtenderForm
from archetypes.pfgextender.testing import layer
from archetypes.pfgextender.testing import populate
from archetypes.pfgextender.testing import FORM_ID
from archetypes.pfgextender.testing import TEXT_ID
from archetypes.pfgextender.interfaces import IPFGExtensible

PloneTestCase.setupPloneSite()

DOCUMENT_ID = 'document'


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testInstalled(self):
        self.failUnless(
            hasattr(self.portal, FormGenTool.id))
        self.failUnless(
            hasattr(self.portal, TOOL_ID))

    def testFactory(self):
        id = self.folder.invokeFactory('Birth', 'birth')
        birth = getattr(self.folder, id)
        self.failUnless(IPFGExtensible.providedBy(birth))

    def testNoHandlerImpact(self):
        self.folder.invokeFactory('FormFolder', 'form')
        self.failUnless('form' in self.folder)

    def testPopulated(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, TOOL_ID)
        self.failUnless(FORM_ID in tool)
        form = queryUtility(IPFGExtenderForm, FORM_ID)
        self.assertEquals(form, getattr(tool, FORM_ID))

    def testFormIsRegistered(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, TOOL_ID)
        form = queryUtility(IPFGExtenderForm, FORM_ID)
        self.assertEquals(form, getattr(tool, FORM_ID))

    def testTypeIsExtended(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        self.folder.invokeFactory('Birth', DOCUMENT_ID)
        document = getattr(self.folder, DOCUMENT_ID)
        schema = document.Schema()
        self.failUnless(TEXT_ID in schema.keys())
        field = schema.getField(TEXT_ID)
        self.assertEquals(field.getName(), TEXT_ID)

    def testFormIsRenamed(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getattr(self.portal, TOOL_ID)
        # savepoint needs to be called to please CopySupport.cb_isMoveable
        transaction.savepoint()
        NEW_FORM_ID = 'new'
        tool.manage_renameObject(FORM_ID, NEW_FORM_ID)
        form = queryUtility(IPFGExtenderForm, NEW_FORM_ID)
        self.assertEquals(form, getattr(tool, NEW_FORM_ID))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite

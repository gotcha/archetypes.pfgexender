import unittest
import transaction

from zope.component import queryUtility

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.tools.formGenTool import FormGenTool
from Products.PloneFormGen.content.form import FormFolder
from Products.Archetypes.Field import StringField
from Products.Archetypes.Field import BooleanField

from archetypes.pfgextender.tool import TOOL_ID
from archetypes.pfgextender.browser.viewlet import FieldsViewlet
from archetypes.pfgextender.interfaces import IPFGExtenderForm
from archetypes.pfgextender.testing import layer
from archetypes.pfgextender.testing import populate
from archetypes.pfgextender.testing import FORM_ID
from archetypes.pfgextender.testing import FIRSTNAME_ID
from archetypes.pfgextender.testing import FIRSTNAME_TITLE
from archetypes.pfgextender.testing import HOME_ID
from archetypes.pfgextender.interfaces import IPFGExtensible

PloneTestCase.setupPloneSite()

EVENT_PORTAL_TYPE = 'Event'
BIRTH_ID = 'birth'


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testInstalled(self):
        self.failUnless(
            hasattr(self.portal, FormGenTool.id))
        self.failUnless(
            hasattr(self.portal, TOOL_ID))

    def testNoImpactOfHandlerOutsideTool(self):
        PFGFORM_ID = 'pfgform'
        self.folder.invokeFactory(FormFolder.portal_type, PFGFORM_ID)
        self.failUnless(PFGFORM_ID in self.folder)
        form = getattr(self.folder, PFGFORM_ID)
        self.failIf(IPFGExtenderForm.providedBy(form))

    def testPopulated(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, TOOL_ID)
        self.failUnless(FORM_ID in tool)

    def testFactory(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        self.failUnless(IPFGExtensible.providedBy(birth))

    def testOldContentMadeExtensible(self):
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        self.failIf(IPFGExtensible.providedBy(birth))
        self.loginAsPortalOwner()
        populate(self.portal)
        self.failUnless(IPFGExtensible.providedBy(birth))

    def testOldContentNoLongerExtensible(self):
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, TOOL_ID)
        tool.resetFormForPortalType(EVENT_PORTAL_TYPE)
        self.failIf(IPFGExtensible.providedBy(birth))

    def testFormIsRegistered(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, TOOL_ID)
        form = getattr(tool, FORM_ID)
        self.failUnless(IPFGExtenderForm.providedBy(form))
        registered = queryUtility(IPFGExtenderForm, EVENT_PORTAL_TYPE)
        self.assertEquals(form, registered)

    def testFormShouldNotBeRenamed(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getattr(self.portal, TOOL_ID)
        # savepoint needs to be called to please CopySupport.cb_isMoveable
        transaction.savepoint()
        NEW_FORM_ID = 'new'
        tool.manage_renameObject(FORM_ID, NEW_FORM_ID)
        self.assertRaises(KeyError, queryUtility,
            IPFGExtenderForm, EVENT_PORTAL_TYPE)

    def testTypeWithWrongRegistration(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getattr(self.portal, TOOL_ID)
        tool.registerFormForPortalType(FORM_ID + 'x', EVENT_PORTAL_TYPE)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        schema = birth.Schema()
        self.failIf(FIRSTNAME_ID in schema.keys())
        self.failIf(HOME_ID in schema.keys())

    def testTypeIsExtended(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        schema = birth.Schema()
        self.failUnless(FIRSTNAME_ID in schema.keys())
        self.failUnless(HOME_ID in schema.keys())

    def testFieldsAreWellConstructed(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        schema = birth.Schema()
        field = schema.getField(FIRSTNAME_ID)
        self.assertEquals(field.getName(), FIRSTNAME_ID)
        self.assertEquals(field.widget.label, FIRSTNAME_TITLE)

    def testBooleanField(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        schema = birth.Schema()
        field = schema.getField(HOME_ID)
        self.failUnless(isinstance(field, BooleanField))

    def testStringField(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        schema = birth.Schema()
        field = schema.getField(FIRSTNAME_ID)
        self.failUnless(isinstance(field, StringField))

    def testViewlet(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        id = self.folder.invokeFactory(EVENT_PORTAL_TYPE, BIRTH_ID)
        birth = getattr(self.folder, id)
        request = self.folder.REQUEST
        viewlet = FieldsViewlet(birth, request, None, None)
        viewlet.update()
        fieldNames = [field.getName() for field in viewlet.getFields()]
        self.failUnless(FIRSTNAME_ID in fieldNames)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite

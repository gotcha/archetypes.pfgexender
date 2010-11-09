from Testing import ZopeTestCase

from zope.component import getSiteManager

from Products.Five import zcml
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.content.form import FormFolder
from Products.PloneFormGen.content.fields import FGStringField
from Products.PloneFormGen.content.fields import FGBooleanField

from collective.testcaselayer import ptc as tcl_ptc

from archetypes import pfgextender
from archetypes.pfgextender.tool import TOOL_ID
from archetypes.pfgextender.fti import registerFormAsUtility


class Layer(tcl_ptc.BasePTCLayer):

    def afterSetUp(self):
        ZopeTestCase.installProduct('PloneFormGen')
        zcml.load_config('testing.zcml', package=pfgextender)
        self.addProfile('archetypes.pfgextender:testing')


layer = Layer(bases=[tcl_ptc.ptc_layer])

FORM_ID = 'birth_form'
FIRSTNAME_ID = 'first_name'
FIRSTNAME_TITLE = 'First Name'
HOME_ID = 'home'
HOME_TITLE = 'Born Home'


def populate(portal):
    tool = getToolByName(portal, TOOL_ID)
    form_id = tool.invokeFactory(FormFolder.portal_type, FORM_ID)
    form = getattr(tool, form_id)
    field_id = form.invokeFactory(FGStringField.portal_type, FIRSTNAME_ID)
    firstname = getattr(form, field_id)
    firstname.setTitle(FIRSTNAME_TITLE)
    field_id = form.invokeFactory(FGBooleanField.portal_type, HOME_ID)
    home = getattr(form, field_id)
    home.setTitle(HOME_TITLE)
    sm = getSiteManager(tool)
    registerFormAsUtility(sm, form, "Birth")

from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.content.form import FormFolder
from Products.PloneFormGen.content.fields import FGStringField
from Products.PloneFormGen.content.fields import FGBooleanField

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting

from archetypes import pfgextender
from archetypes.pfgextender.tool import TOOL_ID


PFGEXTENDER = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=pfgextender,
    gs_profile_id='archetypes.pfgextender:testing',
    additional_z2_products=('Products.PloneFormGen',),
    name="PFGEXTENDER")

PFGEXTENDER_INTEGRATION = IntegrationTesting(
    bases=(PFGEXTENDER,), name="PFGEXTENDER_INTEGRATION")

PFGEXTENDER_FUNCTIONAL = FunctionalTesting(
    bases=(PFGEXTENDER,), name="PFGEXTENDER_FUNCTIONAL")


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
    tool.registerFormForPortalType(form_id, "Event")

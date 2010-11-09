from Testing import ZopeTestCase

from Products.Five import zcml
from Products.CMFCore.utils import getToolByName

from collective.testcaselayer import ptc as tcl_ptc

from archetypes import pfgextender


class Layer(tcl_ptc.BasePTCLayer):

    def afterSetUp(self):
        ZopeTestCase.installProduct('PloneFormGen')
        zcml.load_config('testing.zcml', package=pfgextender)
        self.addProfile('archetypes.pfgextender:testing')


layer = Layer(bases=[tcl_ptc.ptc_layer])

FORM_ID = 'test_form'
TEXT_ID = 'first_name'


def populate(portal):
    tool = getToolByName(portal, 'pfgextender_tool')
    tool.invokeFactory('FormFolder', FORM_ID)
    form = getattr(tool, FORM_ID)
    form.invokeFactory('FormTextField', TEXT_ID)
    text = getattr(form, TEXT_ID)
    text.setTitle('First Name')

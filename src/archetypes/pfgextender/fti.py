from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from archetypes.pfgextender.interfaces import IPFGExtensible
from archetypes.pfgextender.tool import TOOL_ID


class MarkingFactoryTypeInformation(DynamicViewTypeInformation):

    _properties = DynamicViewTypeInformation._properties + (
        {'id': 'pfgform_id', 'type': 'string', 'mode': 'w',
          'label': 'PloneFormGen Form id'},)

    pfgform_id = ''
    security = ClassSecurityInfo()

    security.declarePrivate('_constructInstance')

    def _setPropValue(self, id, value):
        """Overwrite to register the IPFGExtenderForm utility
        """
        DynamicViewTypeInformation._setPropValue(self, id,
            value)
        if id == 'pfgform_id':
            self.registerFormAsUtility()

    def registerFormAsUtility(self):
        tool = getToolByName(self, TOOL_ID)
        portal_type = self.getId()
        tool.registerFormForPortalType(self.pfgform_id, portal_type)

    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type."""
        new_ob = super(MarkingFactoryTypeInformation, self)._constructInstance(
            container, id, *args, **kw)
        alsoProvides(new_ob, IPFGExtensible)
        return new_ob

InitializeClass(MarkingFactoryTypeInformation)

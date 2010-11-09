from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface import alsoProvides
from zope.component import getSiteManager

from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from archetypes.pfgextender.interfaces import IPFGExtensible
from archetypes.pfgextender.interfaces import IPFGExtenderForm


def registerFormAsUtility(sm, pfgForm, portal_type):
    registered = sm.queryUtility(IPFGExtenderForm, name=portal_type)
    if registered is not pfgForm:
        if registered is not None:
            sm.unregisterUtility(registered, IPFGExtenderForm,
                name=portal_type)
        sm.registerUtility(pfgForm, IPFGExtenderForm, name=portal_type)


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
            portal_types = getToolByName(self, 'portal_types')
            pfgForm = portal_types.get(self.pfgform_id, None)
            if pfgForm is not None:
                portal_type = self.getId()
                sm = getSiteManager(portal_types)
                registerFormAsUtility(sm, pfgForm, portal_type)

    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type."""
        new_ob = super(MarkingFactoryTypeInformation, self)._constructInstance(
            container, id, *args, **kw)
        alsoProvides(new_ob, IPFGExtensible)
        return new_ob

InitializeClass(MarkingFactoryTypeInformation)

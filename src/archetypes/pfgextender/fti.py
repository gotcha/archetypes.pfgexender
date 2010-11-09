from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface import alsoProvides

from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation

from archetypes.pfgextender.interfaces import IPFGExtensible


class MarkingFactoryTypeInformation(DynamicViewTypeInformation):

    _properties = DynamicViewTypeInformation._properties + (
        {'id': 'pfgform_id', 'type': 'string', 'mode': 'w',
          'label': 'PloneFormGen Form id'},)

    pfgform_id = ''
    security = ClassSecurityInfo()

    security.declarePrivate('_constructInstance')

    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type."""
        new_ob = super(MarkingFactoryTypeInformation, self)._constructInstance(
            container, id, *args, **kw)
        alsoProvides(new_ob, IPFGExtensible)
        new_ob.pfgform_id = self.pfgform_id
        return new_ob

InitializeClass(MarkingFactoryTypeInformation)

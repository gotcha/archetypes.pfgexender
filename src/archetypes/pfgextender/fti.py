from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface.interfaces import IInterface
from zope.interface import alsoProvides
from zope.dottedname.resolve import resolve

from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation


class MarkingFactoryTypeInformation(DynamicViewTypeInformation):

    _properties = DynamicViewTypeInformation._properties + (
        {'id': 'marking_interface', 'type': 'string', 'mode': 'w',
          'label': 'Interface put on created instances'},)

    marking_interface = ''
    security = ClassSecurityInfo()

    def getMarkingInterface(self):
        if self.marking_interface == '':
            return None
        else:
            interface = resolve(self.marking_interface)
            if not IInterface.providedBy(interface):
                raise TypeError(
                    "Object resolved from [%s] is not an Interface" %
                    self.marking_interface)
            return interface

    security.declarePrivate('_constructInstance')

    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type."""
        new_ob = super(MarkingFactoryTypeInformation, self)._constructInstance(
            container, id, *args, **kw)
        marking_interface = self.getMarkingInterface()
        if marking_interface is not None:
            alsoProvides(new_ob, marking_interface)
        return new_ob

InitializeClass(MarkingFactoryTypeInformation)

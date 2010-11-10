from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.component import getSiteManager

from archetypes.pfgextender.tool import PFGExtenderTool
from archetypes.pfgextender.tool import makePFGExtensible
from archetypes.pfgextender.interfaces import IPFGExtenderForm


def movedPloneFormGenForm(obj, event):
    """registered for IPloneFormGenForm
    """
    if isinstance(event.newParent, PFGExtenderTool):
        alsoProvides(obj, IPFGExtenderForm)


def movedPFGExtenderForm(obj, event):
    """registered for IPFGExtenderForm
    """
    if not isinstance(event.newParent, PFGExtenderTool):
        noLongerProvides(obj, IPFGExtenderForm)


def madeExtensible(obj, event):
    """registered for IBaseObject
    """
    portal_type = obj.portal_type
    sm = getSiteManager(obj)
    extender = sm.queryUtility(IPFGExtenderForm, name=portal_type)
    if extender is not None:
        makePFGExtensible(obj)

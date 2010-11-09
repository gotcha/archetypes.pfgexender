from zope.component import getSiteManager
from zope.interface import alsoProvides

from archetypes.pfgextender.tool import PFGExtenderTool
from archetypes.pfgextender.interfaces import IPFGExtenderForm


def movedPloneFormGenForm(obj, event):
    """registered for IPloneFormGenForm
    """
    if isinstance(event.newParent, PFGExtenderTool):
        sm = getSiteManager(obj)
        alsoProvides(obj, IPFGExtenderForm)
        sm.registerUtility(obj, provided=IPFGExtenderForm, name=event.newName)


def movedPFGExtenderForm(obj, event):
    """registered for IPFGExtenderForm
    """
    sm = getSiteManager(obj)
    if isinstance(event.oldParent, PFGExtenderTool):
        sm.unregisterUtility(obj, provided=IPFGExtenderForm,
            name=event.oldName)
    if isinstance(event.newParent, PFGExtenderTool):
        sm.registerUtility(obj, provided=IPFGExtenderForm, name=event.newName)

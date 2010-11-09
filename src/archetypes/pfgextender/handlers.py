from zope.component import getSiteManager
from zope.interface import alsoProvides

from archetypes.pfgextender.tool import PFGExtenderTool
from archetypes.pfgextender.interfaces import IPFGExtenderForm


def addedForm(obj, event):
    """registered for IPloneFormGenForm
    """
    parent = event.newParent
    if isinstance(parent, PFGExtenderTool):
        alsoProvides(obj, IPFGExtenderForm)
        sm = getSiteManager(obj)
        sm.registerUtility(obj, provided=IPFGExtenderForm, name=obj.getId())


def movedForm(obj, event):
    """registered for IPFGExtenderForm
    """
    parent = event.oldParent
    sm = getSiteManager(obj)
    if isinstance(parent, PFGExtenderTool):
        sm.unregisterUtility(obj, provided=IPFGExtenderForm,
            name=event.oldName)
    parent = event.newParent
    if isinstance(parent, PFGExtenderTool):
        sm.registerUtility(obj, provided=IPFGExtenderForm, name=event.newName)

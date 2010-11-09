from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from archetypes.pfgextender.tool import PFGExtenderTool
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

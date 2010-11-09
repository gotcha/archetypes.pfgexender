from zope.component import getSiteManager
from zope.interface import alsoProvides

from Products.PloneFormGen.interfaces import IPloneFormGenForm

from archetypes.pfgextender.tool import PFGExtenderTool
from archetypes.pfgextender.interfaces import IPFGExtenderForm


def addedForm(obj, event):
    parent = event.newParent
    if not isinstance(parent, PFGExtenderTool):
        return
    if not IPloneFormGenForm.providedBy(obj):
        return
    alsoProvides(obj, IPFGExtenderForm)
    sm = getSiteManager(obj)
    sm.registerUtility(obj, provided=IPFGExtenderForm, name=obj.getId())

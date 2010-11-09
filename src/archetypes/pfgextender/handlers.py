from zope.component import getSiteManager

from Products.PloneFormGen.interfaces import IPloneFormGenForm

from archetypes.pfgextender.tool import PFGExtenderTool


def addedForm(obj, event):
    parent = event.newParent
    if not isinstance(parent, PFGExtenderTool):
        return
    sm = getSiteManager(obj)
    sm.registerUtility(obj, IPloneFormGenForm)

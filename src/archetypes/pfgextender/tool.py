from AccessControl import ClassSecurityInfo

from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.component import getSiteManager

from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.content.form import FormFolder

from archetypes.pfgextender.interfaces import IPFGExtenderForm
from archetypes.pfgextender.interfaces import IPFGExtensible

TOOL_ID = 'portal_pfgextender'


def makePFGExtensible(obj):
    alsoProvides(obj, IPFGExtensible)


def noLongerPFGExtensible(obj):
    noLongerProvides(obj, IPFGExtensible)


class PFGExtenderTool(UniqueObject, PortalFolder):

    id = TOOL_ID
    meta_type = 'PFGExtender'
    portal_type = 'PFGExtender'
    title = 'PFGExtender Forms'
    plone_tool = True
    security = ClassSecurityInfo()

    displayContentsTab = False

    allowed_types = [FormFolder.portal_type]

    def registerFormForPortalType(self, form_id, portal_type):
        self.makeExistingContentAsExtensible(portal_type)
        pfgForm = self.get(form_id, None)
        sm = getSiteManager(self)
        registered = sm.queryUtility(IPFGExtenderForm, name=portal_type)
        if registered is not pfgForm:
            if registered is not None:
                sm.unregisterUtility(registered, IPFGExtenderForm,
                    name=portal_type)
            sm.registerUtility(pfgForm, IPFGExtenderForm, name=portal_type)

    def resetFormForPortalType(self, portal_type):
        self.makeExistingContentNoLongerExtensible(portal_type)
        sm = getSiteManager(self)
        registered = sm.queryUtility(IPFGExtenderForm, name=portal_type)
        if registered is not None:
            sm.unregisterUtility(registered, IPFGExtenderForm,
                name=portal_type)

    def makeExistingContentAsExtensible(self, portal_type):
        portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog(portal_type=portal_type)
        for brain in brains:
            obj = brain.getObject()
            makePFGExtensible(obj)

    def makeExistingContentNoLongerExtensible(self, portal_type):
        portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog(portal_type=portal_type)
        for brain in brains:
            obj = brain.getObject()
            noLongerPFGExtensible(obj)

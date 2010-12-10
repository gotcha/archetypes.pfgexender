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
from archetypes.pfgextender import PfgExtenderFactory as _

TOOL_ID = 'portal_pfgextender'


def makePFGExtensible(obj):
    alsoProvides(obj, IPFGExtensible)


def noLongerPFGExtensible(obj):
    noLongerProvides(obj, IPFGExtensible)


class PFGExtenderTool(UniqueObject, PortalFolder):

    id = TOOL_ID
    meta_type = 'PFGExtender'
    portal_type = 'PFGExtender'
    Title = _('Extension Forms')
    plone_tool = True
    security = ClassSecurityInfo()

    displayContentsTab = False

    allowed_types = [FormFolder.portal_type]

    def registerFormForPortalType(self, form_id, portal_type):
        newForm = self.get(form_id, None)
        if newForm is None:
            self.resetFormForPortalType(portal_type)
        else:
            self.makeExistingContentAsExtensible(portal_type)
            sm = getSiteManager(self)
            currentForm = sm.queryUtility(IPFGExtenderForm, name=portal_type)
            # register new form only if there is a change
            if newForm is not currentForm:
                # unregister only if there is a current registration
                if currentForm is not None:
                    sm.unregisterUtility(provided=IPFGExtenderForm,
                        name=portal_type)
                sm.registerUtility(newForm, IPFGExtenderForm, name=portal_type)

    def resetFormForPortalType(self, portal_type):
        self.makeExistingContentNoLongerExtensible(portal_type)
        registered = self.getRegisteredFormForPortalType(portal_type)
        if registered is not None:
            sm = getSiteManager(self)
            sm.unregisterUtility(provided=IPFGExtenderForm,
                name=portal_type)

    def getRegisteredFormForPortalType(self, portal_type):
        sm = getSiteManager(self)
        registered = sm.queryUtility(IPFGExtenderForm, name=portal_type)
        return registered

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

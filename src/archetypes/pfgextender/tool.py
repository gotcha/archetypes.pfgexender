from AccessControl import ClassSecurityInfo

from zope.component import getSiteManager

from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject
from Products.PloneFormGen.content.form import FormFolder

from archetypes.pfgextender.interfaces import IPFGExtenderForm

TOOL_ID = 'portal_pfgextender'


class PFGExtenderTool(UniqueObject, PortalFolder):

    id = TOOL_ID
    meta_type = 'PFGExtender'
    portal_type = 'PFGExtender'
    title = 'PFGExtender Forms'
    plone_tool = True
    security = ClassSecurityInfo()

    allowed_types = [FormFolder.portal_type]

    def registerFormForPortalType(self, form_id, portal_type):
        pfgForm = self.get(form_id, None)
        sm = getSiteManager(self)
        registered = sm.queryUtility(IPFGExtenderForm, name=portal_type)
        if registered is not pfgForm:
            if registered is not None:
                sm.unregisterUtility(registered, IPFGExtenderForm,
                    name=portal_type)
            sm.registerUtility(pfgForm, IPFGExtenderForm, name=portal_type)

from AccessControl import ClassSecurityInfo

from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject

TOOL_ID = 'portal_pfgextender'

class PFGExtenderTool(UniqueObject, PortalFolder):

    id = TOOL_ID
    meta_type = 'PFGExtender'
    portal_type = 'PFGExtender'
    title = 'PFGExtender Forms'
    plone_tool = True
    security = ClassSecurityInfo()

    allowed_types = ['FormFolder']

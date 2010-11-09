from AccessControl import ClassSecurityInfo

from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject


class PFGExtenderTool(UniqueObject, PortalFolder):

    id = 'pfgextender_tool'
    meta_type = 'PFGExtender'
    portal_type = 'PFGExtender'
    title = 'PFGExtender Forms'
    plone_tool = True
    security = ClassSecurityInfo()

    allowed_types = ['FormFolder']

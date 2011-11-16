from zope.i18nmessageid import MessageFactory

from Products.CMFCore import utils
from Products.Archetypes.public import process_types, listTypes
from Products.PloneFormGen.config import ADD_CONTENT_PERMISSION


PfgExtenderFactory = MessageFactory('pfgextender')

PROJECTNAME = 'archetypes.pfgextender'


def initialize(context):

    import form
    import tool

    form, tool  # make pyflakes happy

    listOfTypes = listTypes(PROJECTNAME)

    content_types, constructors, ftis = process_types(
        listOfTypes,
        PROJECTNAME)
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        permission = ADD_CONTENT_PERMISSION
        utils.ContentInit(
            kind,
            content_types=(atype,),
            permission=permission,
            extra_constructors=(constructor,),
            fti=ftis,
            ).initialize(context)

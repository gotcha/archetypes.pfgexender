from Products.PloneFormGen.content.form import FormFolder

from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder

from archetypes.pfgextender import PROJECTNAME


class ExtFormFolder(FormFolder):

    meta_type = 'ExtFormFolder'
    portal_type = 'ExtFormFolder'
    archetype_name = 'Extension Form Folder'

    def initializeArchetype(self, **kwargs):
        ATFolder.initializeArchetype(self, **kwargs)

registerATCT(ExtFormFolder, PROJECTNAME)

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase

from archetypes.schemaextender.interfaces import ISchemaExtender


class FieldsViewlet(ViewletBase):
    index = ViewPageTemplateFile('fields.pt')

    def getFields(self):
        extender = ISchemaExtender(self.context)
        return extender.getFields()

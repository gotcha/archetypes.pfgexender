from zope.component import getUtility

from Products.Archetypes.Field import TextField as BaseField
from Products.PloneFormGen.content.fieldsBase import BaseFormField
from Products.PloneFormGen.interfaces import IPloneFormGenForm

from archetypes.schemaextender.field import BaseExtensionField


class TextField(BaseExtensionField, BaseField):
    pass


def makeATFieldFromPFGField(pfgField):
    return TextField(pfgField.getId())


class Extender(object):

    def __init__(self, context):
        self.context = context

    def getFields(self):
        pfgForm = getUtility(IPloneFormGenForm)
        fields = [item for item in pfgForm.objectValues()
            if isinstance(item, BaseFormField)]
        return [
            makeATFieldFromPFGField(field) for field in fields]

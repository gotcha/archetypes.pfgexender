from zope.component import queryUtility

from Products.Archetypes.Field import TextField as BaseField
from Products.PloneFormGen.content.fieldsBase import BaseFormField

from archetypes.schemaextender.field import BaseExtensionField

from archetypes.pfgextender.interfaces import IPFGExtensible
from archetypes.pfgextender.interfaces import IPFGExtenderForm


class TextField(BaseExtensionField, BaseField):
    pass


def makeATFieldFromPFGField(pfgField):
    return TextField(pfgField.getId())


class Extender(object):
    """Extend archetypes schema with fields constructed from the fields found
    in a PloneFormGen form. That form is queried by name.
    """

    def __init__(self, context):
        self.context = context

    def getFields(self):
        extensible = IPFGExtensible(self.context)
        pfgform_id = extensible.pfgform_id
        pfgForm = queryUtility(IPFGExtenderForm, name=pfgform_id)
        if pfgForm is None:
            return []
        fields = [item for item in pfgForm.objectValues()
            if isinstance(item, BaseFormField)]
        return [
            makeATFieldFromPFGField(field) for field in fields]

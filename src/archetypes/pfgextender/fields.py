from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.component.factory import Factory
from zope.component import getGlobalSiteManager
from zope.component import ComponentLookupError

from Products.Archetypes.Field import TextField as BaseTextField

from Products.PloneFormGen.content.fields import FGStringField

from archetypes.schemaextender.field import BaseExtensionField


def getFactoryName(pfgClass):
    return pfgClass.__module__ + '.' + pfgClass.__name__


def makeATFieldFromPFGField(pfgField):
    pfgClass = pfgField.__class__
    factoryName = getFactoryName(pfgClass)
    try:
        obj = createObject(factoryName, pfgField)
        return obj
    except ComponentLookupError:
        return None


def registerFactory(factory, pfgClass):
    factoryName = getFactoryName(pfgClass)
    gsm = getGlobalSiteManager()
    gsm.registerUtility(factory, IFactory, factoryName)


class TextField(BaseExtensionField, BaseTextField):

    def __init__(self, pfgField):
        descriptor = dict()
        descriptor['label'] = pfgField.Title()
        descriptor['description'] = pfgField.Description()
        widgetClass = BaseTextField._properties['widget']
        widget = widgetClass(**descriptor)
        descriptor = dict()
        descriptor['name'] = pfgField.getId()
        descriptor['widget'] = widget
        BaseTextField.__init__(self, **descriptor)


textFieldFactory = Factory(TextField)

registerFactory(textFieldFactory, FGStringField)

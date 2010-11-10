from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.component.factory import Factory
from zope.component import getGlobalSiteManager
from zope.component import ComponentLookupError

from Products.Archetypes.Field import StringField as BaseStringField
from Products.Archetypes.Field import BooleanField as BaseBooleanField

from Products.PloneFormGen.content.fields import FGStringField
from Products.PloneFormGen.content.fields import FGBooleanField

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


class ExtensionField(BaseExtensionField):
    """base class for fields created from PFG fields"""

    def instantiate(self, pfgField, ATFieldClass):
        widgetClass = ATFieldClass._properties['widget']
        kwargs = self.getConstructorKwargs(pfgField, widgetClass)
        ATFieldClass.__init__(self, **kwargs)

    def getConstructorKwargs(self, pfgField, widgetClass):
        kwargs = dict()
        kwargs['label'] = pfgField.Title()
        kwargs['description'] = pfgField.Description()
        widget = widgetClass(**kwargs)
        kwargs = dict()
        kwargs['name'] = pfgField.getId()
        kwargs['widget'] = widget
        return kwargs


class StringField(ExtensionField, BaseStringField):

    def __init__(self, pfgField):
        self.instantiate(pfgField, BaseStringField)


stringFieldFactory = Factory(StringField)
registerFactory(stringFieldFactory, FGStringField)


class BooleanField(ExtensionField, BaseBooleanField):

    def __init__(self, pfgField):
        self.instantiate(pfgField, BaseBooleanField)

booleanFieldFactory = Factory(BooleanField)
registerFactory(booleanFieldFactory, FGBooleanField)

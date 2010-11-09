from zope.interface import Interface
from zope.schema import TextLine

from Products.PloneFormGen.interfaces import IPloneFormGenForm


class IPFGExtensible(Interface):
    """If an instance provides IPFGExtensible, its
    schema is extended ``archetypes.pfgextender.extender.Extender``.
    """

    pfgform_id = TextLine(title=u'PloneFormGen Form Id',
        description=u'Id of the PloneFormGen form used to extend the schema',
        required=True)


class IPFGExtenderForm(IPloneFormGenForm):
    pass

from Products.CMFCore.browser.typeinfo import FactoryTypeInformationAddView
from archetypes.pfgextender.fti import MarkingFactoryTypeInformation


class MarkingFactoryTypeInformationAddView(FactoryTypeInformationAddView):

    """Add view for MarkingFactoryTypeInformation.
    """

    klass = MarkingFactoryTypeInformation

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.i18n import translate

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.controlpanel.form import ControlPanelView

from archetypes.pfgextender.tool import TOOL_ID
from archetypes.pfgextender import PfgExtenderFactory as _


NO_EXTENSION_ID = "no_extension"


class TypesControlPanel(ControlPanelView):

    # Actions

    template = ViewPageTemplateFile('types.pt')

    @property
    @memoize
    def type_id(self):
        type_id = self.request.get('type_id', None)
        if type_id is None:
            type_id = ''
        return type_id

    @property
    @memoize
    def fti(self):
        type_id = self.type_id
        portal_types = getToolByName(self.context, 'portal_types')
        return getattr(portal_types, type_id)

    def __call__(self):
        """Perform the update and redirect if necessary, or render the page
        """
        postback = True

        form = self.request.form
        submitted = form.get('form.submitted', False)
        cancel_button = form.get('form.button.Cancel', None) is not None
        save_button = form.get('form.button.Save', None) is not None
        type_id = form.get('old_type_id', None)
        form_id = form.get('form_id', None)

        if submitted and save_button:
            if type_id:
                self.applyNewForm(type_id, form_id)
        elif cancel_button:
            self.request.response.redirect(self.context.absolute_url() + \
                                           '/plone_control_panel')
            postback = False

        if postback:
            return self.template()

    def applyNewForm(self, type_id, form_id):
        portal_pfgextender = getToolByName(self.context, TOOL_ID)
        if form_id == NO_EXTENSION_ID:
            portal_pfgextender.resetFormForPortalType(type_id)
            msg = _("content_type_no_more_extended",
                u"The content type is not extended anymore.")
        elif form_id:
            portal_pfgextender.registerFormForPortalType(form_id=form_id,
                portal_type=type_id)
            msg = _("content_type_extension_updated",
                u"The content type extension form has been modified")
        IStatusMessage(self.request).addStatusMessage(msg, type='info')

    @memoize
    def selectable_types(self):
        vocab_factory = getUtility(IVocabularyFactory,
            name="plone.app.vocabularies.ReallyUserFriendlyTypes")
        types = []
        for v in vocab_factory(self.context):
            portal_types = getToolByName(self.context, 'portal_types')
            fti = getattr(portal_types, v.value)
            if fti.product in ['PloneFormGen', 'archetypes.pfgextender']:
                continue
            if v.title:
                title = translate(v.title, context=self.request)
            else:
                title = translate(v.token, domain='plone',
                    context=self.request)
            types.append(dict(id=v.value, title=title))

        def _key(v):
            return v['title']
        types.sort(key=_key)
        return types

    def get_forms(self):
        portal_pfgextender = getToolByName(self.context, TOOL_ID)
        is_registered = self.is_selected_type_registered()
        no_extension = dict(id=NO_EXTENSION_ID, title=_("No extension"),
            selected=not is_registered)
        result = [no_extension]
        for form_id in portal_pfgextender.objectIds():
            form = getattr(portal_pfgextender, form_id)
            title = form.Title()
            selected = is_registered and (form_id ==
            self.selected_type_form().getId())
            result.append(dict(id=form_id, title=title, selected=selected))
        return result

    def selected_type_form(self):
        portal_pfgextender = getToolByName(self.context, TOOL_ID)
        return portal_pfgextender.getRegisteredFormForPortalType(
            self.fti.getId())

    def is_selected_type_registered(self):
        return self.selected_type_form() is not None

    def selected_type_title(self):
        return self.fti.Title()

    def selected_type_description(self):
        return self.fti.Description()

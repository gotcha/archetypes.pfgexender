from Acquisition import aq_inner

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.i18n import translate

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.form import ControlPanelView


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
        context = aq_inner(self.context)

        form = self.request.form
        submitted = form.get('form.submitted', False)
        save_button = form.get('form.button.Save', None) is not None
        cancel_button = form.get('form.button.Cancel', None) is not None
        type_id = form.get('old_type_id', None)

        if submitted and not cancel_button:
            if type_id:
                pass
        elif cancel_button:
            self.request.response.redirect(self.context.absolute_url() + \
                                           '/plone_control_panel')
            postback = False

        if postback:
            return self.template()

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

    def selected_type_title(self):
        return self.fti.Title()

    def selected_type_description(self):
        return self.fti.Description()

from plone.app.layout.viewlets.common import ContentViewsViewlet as ViewletBase


class ContentViewsViewlet(ViewletBase):

    def prepareObjectTabs(self):
        result = super(ContentViewsViewlet, self).prepareObjectTabs()
        return [item for item in result if item['id'] != "local_roles"]

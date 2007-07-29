##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Five-compatible version of ObjectWidget

This is needed because ObjectWidget uses ViewPageTemplateFile whose
macro definition is unfortunately incompatible with ZopeTwoPageTemplateFile.
So this subclass uses ZopeTwoPageTemplateFile for the template that renders
the widget's sub-editform.

$Id$
"""
import zope.app.form.browser.objectwidget
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass as initializeClass
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ObjectWidgetView(zope.app.form.browser.objectwidget.ObjectWidgetView):
    security = ClassSecurityInfo()
    security.declareObjectPublic()

    template = ViewPageTemplateFile('objectwidget.pt')

initializeClass(ObjectWidgetView)

class ObjectWidgetClass(zope.app.form.browser.objectwidget.ObjectWidget):

    def __init__(self, context, request, factory, **kw):
        super(ObjectWidgetClass, self).__init__(context, request, factory, **kw)
        self.view = ObjectWidgetView(self, request)

    def setRenderedValue(self, value):
        """Slightly more robust re-implementation this method."""
        # re-call setupwidgets with the content
        self._setUpEditWidgets()
        for name in self.names:
            val = getattr(value, name, None)
            if val is None:
                # this is where we are more robust than Zope 3.2's
                # object widget: we supply subwidgets with the default
                # from the schema, not None (Zope 3.2's list widget
                # breaks when the rendered value is None)
                val = self.context.schema[name].default
            self.getSubWidget(name).setRenderedValue(val)

ObjectWidget = ObjectWidgetClass

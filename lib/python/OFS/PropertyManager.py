##############################################################################
# 
# Zope Public License (ZPL) Version 1.0
# -------------------------------------
# 
# Copyright (c) Digital Creations.  All rights reserved.
# 
# This license has been certified as Open Source(tm).
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions in source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 
# 3. Digital Creations requests that attribution be given to Zope
#    in any manner possible. Zope includes a "Powered by Zope"
#    button that is installed by default. While it is not a license
#    violation to remove this button, it is requested that the
#    attribution remain. A significant investment has been put
#    into Zope, and this effort will continue if the Zope community
#    continues to grow. This is one way to assure that growth.
# 
# 4. All advertising materials and documentation mentioning
#    features derived from or use of this software must display
#    the following acknowledgement:
# 
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
# 
#    In the event that the product being advertised includes an
#    intact Zope distribution (with copyright and license included)
#    then this clause is waived.
# 
# 5. Names associated with Zope or Digital Creations must not be used to
#    endorse or promote products derived from this software without
#    prior written permission from Digital Creations.
# 
# 6. Modified redistributions of any form whatsoever must retain
#    the following acknowledgment:
# 
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
# 
#    Intact (re-)distributions of any official Zope release do not
#    require an external acknowledgement.
# 
# 7. Modifications are encouraged but must be packaged separately as
#    patches to official Zope releases.  Distributions that do not
#    clearly separate the patches from the original work must be clearly
#    labeled as unofficial distributions.  Modifications which do not
#    carry the name Zope may be packaged in any form, as long as they
#    conform to all of the clauses above.
# 
# 
# Disclaimer
# 
#   THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS ``AS IS'' AND ANY
#   EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL CREATIONS OR ITS
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
#   USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#   OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#   SUCH DAMAGE.
# 
# 
# This software consists of contributions made by Digital Creations and
# many individuals on behalf of Digital Creations.  Specific
# attributions are listed in the accompanying credits file.
# 
##############################################################################

"""Property management"""
__version__='$Revision: 1.28 $'[11:-2]

import ExtensionClass, Globals
import ZDOM
from PropertySheets import DefaultPropertySheets, vps
from ZPublisher.Converters import type_converters
from Globals import HTMLFile, MessageDialog
from string import find,join,lower,split
from DocumentTemplate import html_quote
from Acquisition import Implicit
from Globals import Persistent
from DateTime import DateTime



class PropertyManager(ExtensionClass.Base, ZDOM.ElementWithAttributes):
    """
    The PropertyManager mixin class provides an object with
    transparent property management. An object which wants to
    have properties should inherit from PropertyManager.

    An object may specify that it has one or more predefined
    properties, by specifying an _properties structure in its
    class::

      _properties=({'id':'title', 'type': 'string', 'mode': 'w'},
                   {'id':'color', 'type': 'string', 'mode': 'w'},
                   )

    The _properties structure is a sequence of dictionaries, where
    each dictionary represents a predefined property. Note that if a
    predefined property is defined in the _properties structure, you
    must provide an attribute with that name in your class or instance
    that contains the default value of the predefined property.

    Each entry in the _properties structure must have at least an 'id'
    and a 'type' key. The 'id' key contains the name of the property,
    and the 'type' key contains a string representing the object's type.
    The 'type' string must be one of the values: 'float', 'int', 'long',
    'string', 'lines', 'text', 'date', 'tokens', 'selection', or
    'multiple section'.

    For 'selection' and 'multiple selection' properties, there is an
    addition item in the property dictionay, 'select_variable' which
    provides the name of a property or method which returns a list of
    strings from which the selection(s) can be chosen.

    Each entry in the _properties structure may *optionally* provide a
    'mode' key, which specifies the mutability of the property. The 'mode'
    string, if present, must contain 0 or more characters from the set
    'w','d'.

    A 'w' present in the mode string indicates that the value of the
    property may be changed by the user. A 'd' indicates that the user
    can delete the property. An empty mode string indicates that the
    property and its value may be shown in property listings, but that
    it is read-only and may not be deleted.

    Entries in the _properties structure which do not have a 'mode' key
    are assumed to have the mode 'wd' (writeable and deleteable).

    To fully support property management, including the system-provided
    tabs and user interfaces for working with properties, an object which
    inherits from PropertyManager should include the following entry in
    its manage_options structure::

      {'label':'Properties', 'action':'manage_propertiesForm',}

    to ensure that a 'Properties' tab is displayed in its management
    interface. Objects that inherit from PropertyManager should also
    include the following entry in its __ac_permissions__ structure::

      ('Manage properties', ('manage_addProperty',
                             'manage_editProperties',
                             'manage_delProperties',
                             'manage_changeProperties',)),
    """

    manage_options=(
        {'label':'Properties', 'action':'manage_propertiesForm',
         'help':('OFSP','Properties.stx')},         
        )
    
    manage_propertiesForm=HTMLFile('properties', globals(),
                                   property_extensible_schema__=1)
    manage_propertyTypeForm=HTMLFile('propertyType', globals())

    title=''
    _properties=({'id':'title', 'type': 'string', 'mode':'w'},)
    _reserved_names=()

    __ac_permissions__=(
        ('Manage properties', ('manage_addProperty',
                               'manage_editProperties',
                               'manage_delProperties',
                               'manage_changeProperties',
                               'manage_propertiesForm',
                               'manage_propertyTypeForm',
                               'manage_changePropertyTypes',
                               )),
        ('Access contents information',
         ('hasProperty', 'propertyIds', 'propertyValues','propertyItems',
          'getProperty', 'getPropertyType', 'propertyMap', ''),
         ('Anonymous', 'Manager'),
         ),
        )

    __propsets__=()
    propertysheets=vps(DefaultPropertySheets)

    def valid_property_id(self, id):
        if not id or id[:1]=='_' or (' ' in id) \
           or hasattr(self.aq_base, id):
            return 0
        return 1

    def getProperty(self, id, d=None):
        """Get the property 'id', returning the optional second 
           argument or None if no such property is found."""
        if self.hasProperty(id):
            return getattr(self, id)
        return d

    def getPropertyType(self, id):
        """Get the type of property 'id', returning None if no
           such property exists"""
        for md in self._properties:
            if md['id']==id:
                return md.get('type', 'string')
        return None

    def _wrapperCheck(self, object):
        # Raise an error if an object is wrapped.
        if hasattr(object, 'aq_base'):
            raise ValueError, 'Invalid property value: wrapped object'
        return

    def _setPropValue(self, id, value):
        self._wrapperCheck(value)
        setattr(self,id,value)

    def _delPropValue(self, id):
        delattr(self,id)

    def _setProperty(self, id, value, type='string'):
        # for selection and multiple selection properties
        # the value argument indicates the select variable
        # of the property
        self._wrapperCheck(value)
        if not self.valid_property_id(id):
            raise 'Bad Request', 'Invalid or duplicate property id'
        if type in ('selection', 'multiple selection'):
            if not hasattr(self, value):
                raise 'Bad Request', 'No select variable %s' % value
            self._properties=self._properties + (
                {'id':id, 'type':type, 'select_variable':value},)
            if type=='selection':
                self._setPropValue(id, '')
            else:
                self._setPropValue(id, [])
        else:
            self._properties=self._properties+({'id':id,'type':type},)
            self._setPropValue(id, value)

    def _updateProperty(self, id, value):
        # Update the value of an existing property. If value
        # is a string, an attempt will be made to convert
        # the value to the type of the existing property.
        self._wrapperCheck(value)
        if not self.hasProperty(id):
            raise 'Bad Request', 'The property %s does not exist' % id
        if type(value)==type(''):
            proptype=self.getPropertyType(id) or 'string'
            if type_converters.has_key(proptype):
                value=type_converters[proptype](value)
        self._setPropValue(id, value)

    def hasProperty(self, id):
        """Return true if object has a property 'id'"""
        for p in self._properties:
            if id==p['id']:
                return 1
        return 0

    def _delProperty(self, id):
        if not self.hasProperty(id):
            raise ValueError, 'The property %s does not exist' % id
        delattr(self,id)
        self._properties=tuple(filter(lambda i, n=id: i['id'] != n,
                                      self._properties))

    def propertyIds(self):
        """Return a list of property ids """
        return map(lambda i: i['id'], self._properties)

    def propertyValues(self):
        """Return a list of actual property objects """
        return map(lambda i,s=self: getattr(s,i['id']), self._properties)

    def propertyItems(self):
        """Return a list of (id,property) tuples """
        return map(lambda i,s=self: (i['id'],getattr(s,i['id'])), 
                                    self._properties)
    def propertyMap(self):
        """Return a tuple of mappings, giving meta-data for properties """
        return self._properties

    def propertyLabel(self, id):
        """Return a label for the given property id
        """
        return id

    def propdict(self):
        dict={}
        for p in self._properties:
            dict[p['id']]=p
        return dict


    # Web interface

    def manage_addProperty(self, id, value, type, REQUEST=None):
        """Add a new property via the web. Sets a new property with
        the given id, type, and value."""
        if type_converters.has_key(type):
            value=type_converters[type](value)
        self._setProperty(id, value, type)
        if REQUEST is not None:
            return self.manage_propertiesForm(self, REQUEST)

    def manage_editProperties(self, REQUEST):
        """Edit object properties via the web."""
        for prop in self._properties:
            name=prop['id']
            if REQUEST.has_key(name):
                if 'w' in prop.get('mode', 'wd'):
                    value=REQUEST.get(name)
                    self._setPropValue(name, value)
        return MessageDialog(
               title  ='Success!',
               message='Your changes have been saved',
               action ='manage_propertiesForm')

    def manage_changeProperties(self, REQUEST=None, **kw):
        """Change existing object properties.

        Change object properties by passing either a mapping object
        of name:value pairs {'foo':6} or passing name=value parameters
        """
        if REQUEST is None:
            props={}
        else:
            props=REQUEST

        if kw:
            for name, value in kw.items():
                props[name]=value

        propdict=self.propdict()
        for name, value in props.items():
            if self.hasProperty(name):
                if not 'w' in propdict[name].get('mode', 'wd'):
                    raise 'BadRequest', '%s cannot be changed' % name
                self._setPropValue(name, value)
        if REQUEST is not None:
            return MessageDialog(
                title  ='Success!',
                message='Your changes have been saved',
                action ='manage_propertiesForm')

    # Note - this is experimental, pending some community input.
    
    def manage_changePropertyTypes(self, old_ids, props, REQUEST=None):
        """Replace one set of properties with another

        Delete all properties that have ids in old_ids, then add a
        property for each item in props.  Each item has a new_id,
        new_value, and new_type.  The type of new_value should match
        new_type.
        """
        err = self.manage_delProperties(old_ids)
        if err:
            if REQUEST is not None:
                return err
            return
        for prop in props:
            self._setProperty(prop.new_id, prop.new_value, prop.new_type)
        if REQUEST is not None:
            return self.manage_propertiesForm(self, REQUEST)
            

    def manage_delProperties(self, ids=None, REQUEST=None):
        """Delete one or more properties specified by 'ids'."""
        if ids is None:
            return MessageDialog(
                   title='No property specified',
                   message='No properties were specified!',
                   action ='./manage_propertiesForm',)
        propdict=self.propdict()
        nd=self._reserved_names
        for id in ids:
            if not hasattr(self.aq_base, id):
                raise 'BadRequest', (
                      'The property <em>%s</em> does not exist' % id)
            if (not 'd' in propdict[id].get('mode', 'wd')) or (id in nd):
                return MessageDialog(
                title  ='Cannot delete %s' % id,
                message='The property <em>%s</em> cannot be deleted.' % id,
                action ='manage_propertiesForm')
            self._delProperty(id)

        if REQUEST is not None:
            return self.manage_propertiesForm(self, REQUEST)




Globals.default__class_init__(PropertyManager)

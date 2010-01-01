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
"""
Use 'structured monkey patching' to enable zope.container event sending for
Zope 2 objects.

$Id$
"""

from OFS.subscribers import deprecatedManageAddDeleteClasses

def setDeprecatedManageAddDelete(class_):
    """Instances of the class will still see their old methods called."""
    deprecatedManageAddDeleteClasses.append(class_)

def cleanUp():
    deprecatedManageAddDeleteClasses[:] = []

def deprecatedManageAddDelete(_context, class_):
    _context.action(
        discriminator=('five:deprecatedManageAddDelete', class_),
        callable=setDeprecatedManageAddDelete,
        args=(class_,),
        )

from zope.testing.cleanup import addCleanUp
addCleanUp(cleanUp)
del addCleanUp

##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""ZClass tests

$Id$
"""

import sys
import unittest
import ZODB.tests.util
import transaction
from zope.testing import doctest


# XXX need to update files to get newer testing package
class FakeModule:
    def __init__(self, name, dict):
        self.__dict__ = dict
        self.__name__ = name


def setUp(test):
    test.globs['some_database'] = ZODB.tests.util.DB()
    module = FakeModule('ZClasses.example', test.globs)
    sys.modules[module.__name__] = module
    
def tearDown(test):
    transaction.abort()
    test.globs['some_database'].close()
    del sys.modules['ZClasses.example']

def test_suite():
    return unittest.TestSuite((

        # To do:
        # - Beef up basic test
        # - Test working with old pickles
        # - Test proper handling of __of__
        # - Test export/import
        
        doctest.DocFileSuite("_pmc.txt", setUp=setUp, tearDown=tearDown),
        doctest.DocFileSuite("ZClass.txt", setUp=setUp, tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


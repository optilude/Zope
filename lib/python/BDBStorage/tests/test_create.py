##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
# 
##############################################################################

# Unit test for database creation

import os
import unittest
import BerkeleyTestBase    



class TestMixin:
    def checkDBHomeExists(self):
        self.failUnless(os.path.isdir(BerkeleyTestBase.DBHOME))


class MinimalCreateTest(BerkeleyTestBase.BerkeleyTestBase,
                        BerkeleyTestBase.MinimalTestBase,
                        TestMixin):
    pass


class FullCreateTest(BerkeleyTestBase.BerkeleyTestBase,
                     BerkeleyTestBase.FullTestBase,
                     TestMixin):
    pass



class FullOpenExistingTest(BerkeleyTestBase.BerkeleyTestBase,
                           BerkeleyTestBase.FullTestBase):
    def checkOpenWithExistingVersions(self):
        version = 'test-version'
        oid = self._storage.new_oid()
        revid = self._dostore(oid, data=7, version=version)
        # Now close the current storage and re-open it
        self._storage.close()
        self._storage = self.ConcreteStorage(BerkeleyTestBase.DBHOME)
        self.assertEqual(self._storage.modifiedInVersion(oid), version)

    def checkOpenAddVersion(self):
        eq = self.assertEqual
        version1 = 'test-version'
        oid1 = self._storage.new_oid()
        revid = self._dostore(oid1, data=7, version=version1)
        # Now close the current storage and re-open it
        self._storage.close()
        self._storage = self.ConcreteStorage(BerkeleyTestBase.DBHOME)
        eq(self._storage.modifiedInVersion(oid1), version1)
        # Now create a 2nd version string, then close/reopen
        version2 = 'new-version'
        oid2 = self._storage.new_oid()
        revid = self._dostore(oid2, data=8, version=version2)
        # Now close the current storage and re-open it
        self._storage.close()
        self._storage = self.ConcreteStorage(BerkeleyTestBase.DBHOME)
        eq(self._storage.modifiedInVersion(oid1), version1)
        # Now create a 2nd version string, then close/reopen
        eq(self._storage.modifiedInVersion(oid2), version2)



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MinimalCreateTest, 'check'))
    suite.addTest(unittest.makeSuite(FullCreateTest, 'check'))
    suite.addTest(unittest.makeSuite(FullOpenExistingTest, 'check'))
    return suite



if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

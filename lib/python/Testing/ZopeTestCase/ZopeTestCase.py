#
# Default test case & fixture for Zope testing
#
# The fixture consists of:
#
#   - a folder (self.folder)
#   - a user folder inside that folder
#   - a default user inside the user folder
#
# The default user is logged in and has the 'Access contents information'
# and 'View' permissions given to his role.
#

# $Id: ZopeTestCase.py,v 1.29 2005/02/09 12:42:40 shh42 Exp $

import base
import functional
import interfaces
import utils

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.Permissions import access_contents_information
from AccessControl.Permissions import view

folder_name = 'test_folder_1_'
user_name = 'test_user_1_'
user_password = 'secret'
user_role = 'test_role_1_'
standard_permissions = [access_contents_information, view]


class ZopeTestCase(base.TestCase):
    '''Base test case for Zope testing'''

    __implements__ = (interfaces.IZopeSecurity,
                      base.TestCase.__implements__)

    _setup_fixture = 1

    def _setup(self):
        '''Sets up the fixture. Framework authors may
           override.
        '''
        if self._setup_fixture:
            self._setupFolder()
            self._setupUserFolder()
            self._setupUser()
            self.login()

    def _setupFolder(self):
        '''Creates and configures the folder.'''
        self.app.manage_addFolder(folder_name)
        self.folder = self.app._getOb(folder_name)
        self.folder._addRole(user_role)
        self.folder.manage_role(user_role, standard_permissions)

    def _setupUserFolder(self):
        '''Creates the user folder.'''
        self.folder.manage_addUserFolder()

    def _setupUser(self):
        '''Creates the default user.'''
        uf = self.folder.acl_users
        uf.userFolderAddUser(user_name, user_password, [user_role], [])

    def _clear(self, call_close_hook=0):
        '''Clears the fixture.'''
        # This code is a wart from the olden days.
        try:
            if base._connections.contains(self.app._p_jar):
                self.app._delObject(folder_name)
        except:
            pass
        base.TestCase._clear(self, call_close_hook)

    # Security interface

    def setRoles(self, roles, name=user_name):
        '''Changes the user's roles.'''
        uf = self.folder.acl_users
        uf.userFolderEditUser(name, None, utils.makelist(roles), [])
        if name == getSecurityManager().getUser().getId():
            self.login(name)

    def setPermissions(self, permissions, role=user_role):
        '''Changes the user's permissions.'''
        self.folder.manage_role(role, utils.makelist(permissions))

    def login(self, name=user_name):
        '''Logs in.'''
        uf = self.folder.acl_users
        user = uf.getUserById(name)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)

    def logout(self):
        '''Logs out.'''
        noSecurityManager()

    # b/w compatibility methods

    def _setRoles(self, roles, name=user_name):
        self.setRoles(roles, name)
    def _setPermissions(self, permissions, role=user_role):
        self.setPermissions(permissions, role)
    def _login(self, name=user_name):
        self.login(name)
    def _logout(self):
        self.logout()


class FunctionalTestCase(functional.Functional, ZopeTestCase):
    '''Base class for functional Zope tests'''

    __implements__ = (functional.Functional.__implements__,
                      ZopeTestCase.__implements__)


# b/w compatibility names
_folder_name = folder_name
_user_name = user_name
_user_role = user_role
_standard_permissions = standard_permissions
from base import app
from base import close
from base import closeConnections


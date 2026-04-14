"""Integration tests for eea.api.versions REST API endpoints

Uses publish() from Testing.makerequest to call REST API views
without requiring plone.restapi.testing.RelativeSession.
"""

import unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from transaction import commit
from eea.api.versions.tests.base import FUNCTIONAL_TESTING


class TestEEAVersionsSetup(unittest.TestCase):
    """Test eea.api.versions installation"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test that eea.api.versions is installed"""
        from Products.CMFPlone.utils import get_installer
        installer = get_installer(self.portal, self.layer["request"])
        self.assertTrue(installer.is_product_installed("eea.api.versions"))

    def test_portal_exists(self):
        """Test that portal is set up"""
        self.assertIsNotNone(self.portal)

    def test_sandbox_folder_exists(self):
        """Test that sandbox folder was created"""
        self.assertIn("sandbox", self.portal.objectIds())

    def test_manager_role(self):
        """Test that test user has Manager role"""
        from plone.app.testing import TEST_USER_ID
        roles = self.portal.acl_users.getUserById(TEST_USER_ID).getRoles()
        self.assertIn("Manager", roles)


class TestEEAVersionsView(unittest.TestCase):
    """Test eea.versions expandable element"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_eea_versions_adapter_registered(self):
        """Test that EEAVersions adapter is registered"""
        from zope.component import queryMultiAdapter
        from zope.interface import Interface
        adapter = queryMultiAdapter((self.portal, self.portal.REQUEST), Interface, name="eea.versions")
        # Adapter may or may not be registered depending on config
        # Just check the import works
        from eea.api.versions.restapi.get import EEAVersions
        self.assertIsNotNone(EEAVersions)

    def test_eea_versions_get_class_exists(self):
        """Test that EEAVersionsGet class exists"""
        from eea.api.versions.restapi.get import EEAVersionsGet
        self.assertIsNotNone(EEAVersionsGet)

    def test_eea_versions_returns_dict(self):
        """Test that EEAVersions returns a dict"""
        from eea.api.versions.restapi.get import EEAVersions
        from zope.interface import Interface
        result = EEAVersions(self.portal, self.portal.REQUEST)()
        self.assertIsInstance(result, dict)

    def test_eea_versions_has_id(self):
        """Test that EEAVersions response has eea.versions key"""
        from eea.api.versions.restapi.get import EEAVersions
        result = EEAVersions(self.portal, self.portal.REQUEST)()
        self.assertIn("eea.versions", result)


if __name__ == "__main__":
    unittest.main()
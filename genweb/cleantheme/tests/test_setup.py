# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from genweb.cleantheme.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of genweb.cleantheme into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if genweb.cleantheme is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('genweb.cleantheme'))

    def test_uninstall(self):
        """Test if genweb.cleantheme is cleanly uninstalled."""
        self.installer.uninstallProducts(['genweb.cleantheme'])
        self.assertFalse(self.installer.isProductInstalled('genweb.cleantheme'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IGenwebCleanthemeLayer is registered."""
        from genweb.cleantheme.interfaces import IGenwebCleanthemeLayer
        from plone.browserlayer import utils
        self.failUnless(IGenwebCleanthemeLayer in utils.registered_layers())

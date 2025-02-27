# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from address import AddressTestCase
from auth import AuthTestCase
from country import CountryTestCase
from currency import CurrencyTestCase
from i18n import I18NTestCase
from routing import RoutingTestCase
from static_file import StaticFileTestCase
from translation import TranslationTestCase
from user import UserTestCase
from website import WebsiteTestCase

from trytond.config import config

# Use NereidModuleTestCase as a wrapper for ModuleTestCase
from nereid.testing import NereidModuleTestCase

# s. #5137
FROM = 'no-reply@localhost'

class NereidBaseTestCase(NereidModuleTestCase):
    "Test Nereid Base module"
    module = 'nereid_base'

    def setUp(self):
        super().setUp()
        reset_from = config.get('email', 'from', default='')
        config.set('email', 'from', FROM)
        self.addCleanup(lambda: config.set('email', 'from', reset_from))

del NereidModuleTestCase

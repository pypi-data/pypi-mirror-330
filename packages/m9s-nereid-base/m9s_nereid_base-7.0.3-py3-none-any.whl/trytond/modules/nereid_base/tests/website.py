# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import json
import unittest

import trytond.tests.test_tryton

from trytond.tests.test_tryton import with_transaction

from nereid.testing import NereidTestCase

from common import setup_objects


class WebsiteTestCase(NereidTestCase):
    'Test Website'

    def setUp(self):
        trytond.tests.test_tryton.activate_module('nereid_base')
        setup_objects(self)

    def setup_defaults(self):
        """
        Setup the defaults
        """
        usd, = self.currency_obj.create([{
            'name': 'US Dollar',
            'code': 'USD',
            'symbol': '$',
            }])
        self.party, = self.party_obj.create([{
            'name': 'MBSolutions',
            }])
        self.company, = self.company_obj.create([{
            'party': self.party,
            'currency': usd,
            }])

        en, = self.language_obj.search([('code', '=', 'en')])
        currency, = self.currency_obj.search([('code', '=', 'USD')])
        locale, = self.nereid_website_locale_obj.create([{
            'code': 'en',
            'language': en,
            'currency': currency,
            }])
        self.nereid_website_obj.create([{
            'name': 'localhost',
            'company': self.company,
            'application_user': 1,
            'default_locale': locale,
            }])

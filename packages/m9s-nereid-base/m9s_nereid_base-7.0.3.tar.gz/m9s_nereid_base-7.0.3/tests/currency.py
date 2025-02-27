# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from common import setup_objects

import trytond.tests.test_tryton

from trytond.tests.test_tryton import with_transaction

from nereid import render_template
from nereid.testing import NereidTestCase


class CurrencyTestCase(NereidTestCase):
    """
    Test Currency
    """

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
            'rates': [('create', [{'rate': Decimal('1')}])],
            }])
        eur, = self.currency_obj.create([{
            'name': 'Euro',
            'code': 'EUR',
            'symbol': 'E',
            'rates': [('create', [{'rate': Decimal('2')}])],
            }])
        self.party, = self.party_obj.create([{
            'name': 'MBSolutions',
            }])
        self.company, = self.company_obj.create([{
            'currency': usd,
            'party': self.party,
            }])
        c1, = self.currency_obj.create([{
            'code': 'C1',
            'symbol': 'C1',
            'name': 'Currency 1',
            'rates': [('create', [{'rate': Decimal('10')}])],

            }])
        c2, = self.currency_obj.create([{
            'code': 'C2',
            'symbol': 'C2',
            'name': 'Currency 2',
            'rates': [('create', [{'rate': Decimal('20')}])],
            }])
        self.lang_currency, = self.currency_obj.create([{
            'code': 'C3',
            'symbol': 'C3',
            'name': 'Currency 3',
            'rates': [('create', [{'rate': Decimal('30')}])],
            }])
        self.currency_obj.create([{
            'code': 'C4',
            'symbol': 'C4',
            'name': 'Currency 4',
            'rates': [('create', [{'rate': Decimal('40')}])],
            }])
        self.website_currencies = [c1, c2]
        self.en, = self.language_obj.search([('code', '=', 'en')])
        self.es, = self.language_obj.search([('code', '=', 'es')])
        self.usd, = self.currency_obj.search([('code', '=', 'USD')])
        self.eur, = self.currency_obj.search([('code', '=', 'EUR')])
        locale_en, locale_es = self.nereid_website_locale_obj.create([{
            'code': 'en',
            'language': self.en,
            'currency': self.usd,
            }, {
            'code': 'es',
            'language': self.es,
            'currency': self.eur,
            }])
        self.nereid_website_obj.create([{
            'name': 'localhost',
            'company': self.company,
            'application_user': 1,
            'default_locale': locale_en.id,
            'locales': [('add', [locale_en.id, locale_es.id])],
            'currencies': [('add', self.website_currencies)],
            }])
        self.templates = {
            'home.jinja':
                '''
                {{ current_locale.currency.id }}
                ''',
                }

    def get_template_source(self, name):
        """
        Return templates
        """
        return self.templates.get(name)

    @with_transaction()
    def test_0010_currency_from_default_locale(self):
        """
        Do not set a currency for the language, and the fail over of
        picking currency from default locale.
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/en/')
            self.assertEqual(rv.status_code, 200)

        self.assertEqual(int(rv.data), self.usd.id)

        with app.test_request_context('/en/'):
            self.assertEqual(self.currency_obj.convert(Decimal('100')),
                Decimal('100'))

    @with_transaction()
    def test_0020_currency_from_locale(self):
        """
        Test and ensure that the currency is based on the locale
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/en/')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(int(rv.data), int(self.usd.id))

            rv = c.get('/es/')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(int(rv.data), int(self.eur.id))

        with app.test_request_context('/en/'):
            self.assertEqual(self.currency_obj.convert(Decimal('100')),
                Decimal('100'))

        with app.test_request_context('/es/'):
            self.assertEqual(self.currency_obj.convert(Decimal('100')),
                Decimal('200'))

    @with_transaction()
    def test_0030_get_currencies(self):
        """
        Test and ensure that get_currencies() works (includes caching)
        """
        self.setup_defaults()
        self.templates = {
            'home.jinja':
                '''
                {{ current_website.get_currencies() }}
                ''',
                }
        app = self.get_app()

        with app.test_request_context('/en/'):
            home_template = render_template('home.jinja')
            self.assertTrue('1' in home_template)

# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
import unittest

import trytond.tests.test_tryton

from trytond.config import config
from trytond.exceptions import UserWarning
from trytond.pool import Pool, PoolMeta
from trytond.tests.test_tryton import with_transaction
from trytond.transaction import Transaction

from nereid import render_template, route
from nereid.contrib.locale import make_lazy_gettext, make_lazy_ngettext
from nereid.testing import POOL as pool
from nereid.testing import NereidTestCase

from common import setup_objects

config.set('email', 'from', 'from@xyz.com')
config.set('database', 'path', '/tmp/temp_tryton_data/')


class StaticFileServingHomePage(metaclass=PoolMeta):
    __name__ = 'nereid.website'

    @classmethod
    @route('/static-file-test')
    def static_file_test(cls):
        static_file_obj = Pool().get('nereid.static.file')

        static_file, = static_file_obj.search([])
        return render_template(
            'home.jinja',
            static_file_obj=static_file_obj,
            static_file_id=static_file.id
        )


class StaticFileTestCase(NereidTestCase):

    @classmethod
    def setUpClass(cls):
        pool.register(StaticFileServingHomePage, module='nereid_base', type_='model')
        pool.init(update=['nereid_base'])

    @classmethod
    def tearDownClass(cls):
        mpool = pool.classes['model'].setdefault('nereid_base', [])
        del(mpool[StaticFileServingHomePage])
        pool.init(update=['nereid_base'])

    def setUp(self):
        trytond.tests.test_tryton.activate_module('nereid_base')
        setup_objects(self)

        self.templates = {
            'home.jinja':
            '''
            {% set static_file = static_file_obj(static_file_id) %}
            {{ static_file.url }}
            ''',
            }

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
            'locales': [('add', [locale.id])],
            }])

    def create_static_file(self, file_memoryview, convert_format=None):
        """
        Creates the static file for testing
        """
        pool = Pool()
        StaticFile = pool.get('nereid.static.file')
        StaticFolder = pool.get('nereid.static.folder')

        folders = StaticFolder.search([('name', '=', 'test')])
        if folders:
            folder, = folders
        else:
            folder, = StaticFolder.create([{
                        'name': 'test',
                        'description': 'Test Folder'
                        }])

        return StaticFile.create([{
            'name': 'test.png',
            'folder': folder,
            'file_binary': file_memoryview,
            'convert_format': convert_format,
            }])[0]

    @with_transaction()
    def test_0010_static_file(self):
        """
        Create a static folder, and a static file
        and check if it can be fetched
        """
        self.setup_defaults()

        file_memoryview = memoryview(b'test-content')
        static_file = self.create_static_file(file_memoryview)

        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/en/static-file/test/test.png')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data.decode('utf-8'), 'test-content')
            self.assertEqual(rv.headers['Content-Type'], 'image/png')

    @with_transaction()
    def test_0020_static_file_url(self):
        self.setup_defaults()

        file_memoryview = memoryview(b'test-content')
        file = self.create_static_file(file_memoryview)
        self.assertFalse(file.url)

        app = self.get_app()
        with app.test_client() as c:
            rv = c.get('/en/static-file-test')
            self.assertEqual(rv.status_code, 200)
            self.assertTrue('/en/static-file/test/test.png' in
                rv.data.decode('utf-8'))

    @with_transaction()
    def test_0030_static_file_convert_format(self):
        self.setup_defaults()

        # Use a real image file, python-magic doesn't cooperate well with
        # memoryview
        img_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'pixel.png')
        with open(img_file, 'rb') as f:
            static_file = self.create_static_file(f.read(),
                convert_format='webp')

        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/en/static-file/test/test.webp')
            self.assertEqual(rv.status_code, 200)
            #self.assertEqual(rv.data.decode('utf-8'), 'test-content')
            self.assertEqual(rv.headers['Content-Type'], 'image/webp')

    @with_transaction()
    def test_0040_static_file_invalid_convert_format(self):
        pool = Pool()
        Warning = pool.get('res.user.warning')
        StaticFile = pool.get('nereid.static.file')

        self.setup_defaults()

        # Use a real image file, python-magic doesn't cooperate well with
        # memoryview
        img_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'pixel.png')

        # Convert to an unsupported format and get the UserWarning
        with self.assertRaises(UserWarning):
            with open(img_file, 'rb') as f:
                static_file = self.create_static_file(f.read(),
                    convert_format='x-xbitmap')

        # Disable the UserWarning
        warning, = Warning.create([{
                    'user': 1,
                    'name': 'image_convert_error.x-xbitmap',
                    'always': True}])
        warning.save()

        # Cleanup all static files to avoid name conflicts
        static_files = StaticFile.search([])
        StaticFile.delete(static_files)

        # Second run with the same unsupported format should save the original
        # file
        with open(img_file, 'rb') as f:
            static_file = self.create_static_file(f.read(),
                convert_format='x-xbitmap')

        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/en/static-file/test/test.png')
            self.assertEqual(rv.status_code, 200)
            #self.assertEqual(rv.data.decode('utf-8'), 'test-content')
            self.assertEqual(rv.headers['Content-Type'], 'image/png')


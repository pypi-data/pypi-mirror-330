# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool

from . import (
    country, currency, model, party, static_file, translation, user, website)

__all__ = ['register']


def register():
    Pool.register(
        party.Address,
        party.Party,
        party.ContactMechanism,
        user.NereidUser,
        user.NereidAnonymousUser,
        website.WebSiteLocale,
        website.WebSite,
        website.WebsiteCountry,
        website.WebsiteCurrency,
        website.WebsiteWebsiteLocale,
        static_file.NereidStaticFolder,
        static_file.NereidStaticFile,
        currency.Currency,
        translation.Translation,
        country.Country,
        country.Subdivision,
        model.ModelData,
        module='nereid_base', type_='model')
    Pool.register(
        party.PartyErase,
        party.PartyReplace,
        translation.TranslationSet,
        translation.TranslationUpdate,
        translation.TranslationClean,
        module='nereid_base', type_='wizard')

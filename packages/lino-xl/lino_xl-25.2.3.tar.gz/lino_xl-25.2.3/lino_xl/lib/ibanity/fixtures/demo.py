# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _


def objects():
    if dd.plugins.ibanity.supplier_id:
        qs = rt.models.contacts.Company.objects.exclude(vat_id="").filter(country__isocode="BE")
        qs.update(is_outbound=True)
        jnl = rt.models.accounting.Journal.get_by_ref("SLS")
        jnl.is_outbound=True
        yield jnl

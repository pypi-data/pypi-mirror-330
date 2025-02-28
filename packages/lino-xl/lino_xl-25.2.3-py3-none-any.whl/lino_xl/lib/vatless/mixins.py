# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Model mixins for `lino_xl.lib.vatless`.


"""

from lino.api import dd


class PartnerDetailMixin(dd.DetailLayout):
    """Defines a panel :attr:`accounting`, to be added as a tab panel to your
    layout's `main` element.

    .. attribute:: accounting

        Shows the tables `vatless.VouchersByPartner` and
        `accounting.MovementsByPartner`.

    """
    if dd.is_installed('accounting'):
        accounting = dd.Panel("""
        payment_term
        vatless.VouchersByPartner
        accounting.MovementsByPartner
        """,
                          label=dd.plugins.accounting.verbose_name)
    else:
        accounting = dd.DummyPanel()

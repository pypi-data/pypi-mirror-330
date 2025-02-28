# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html

# from datetime import datetime
from dateutil.parser import isoparse

from django.utils import timezone
from django.conf import settings
from django.db import models
from lino.api import dd, rt, _
from lino import logger
from lino.mixins import Contactable, Phonable
from lino.modlib.checkdata.choicelists import Checker
# from lino.mixins.periods import DateRange
from lino_xl.lib.accounting.choicelists import VoucherStates
from lino_xl.lib.contacts.mixins import ContactRelated
from lino_xl.lib.countries.mixins import AddressLocation
from lino_xl.lib.vat.choicelists import VatSubjectable

if dd.plugins.ibanity.with_suppliers:
    from .suppliers import *

if dd.plugins.ibanity.supplier_id:
    from .documents import *

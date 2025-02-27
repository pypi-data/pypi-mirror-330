# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class NereidPaymentGatewayTestCase(ModuleTestCase):
    "Test Nereid Payment Gateway module"
    module = 'nereid_payment_gateway'


del ModuleTestCase

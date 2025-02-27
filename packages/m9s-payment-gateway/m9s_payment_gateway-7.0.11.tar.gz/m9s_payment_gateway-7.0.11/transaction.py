# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import logging
import re
import time

from datetime import datetime, timezone
from uuid import uuid4

import yaml

from babel import dates, numbers

from trytond.config import config
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.model import (
    DeactivableMixin, ModelSQL, ModelView, Workflow, fields)
from trytond.modules.currency.fields import Monetary
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Bool, Eval, If
from trytond.transaction import Transaction, _TransactionLockError
from trytond.wizard import (
    Button, StateAction, StateTransition, StateView, Wizard)

READONLY_IF_NOT_DRAFT = {'readonly': Eval('state') != 'draft'}
STATES = {
    'readonly': ~Eval('active', True),
}

_retry = config.getint('database', 'retry')

logger = logging.getLogger(__name__)


class PaymentGateway(DeactivableMixin, ModelSQL, ModelView):
    """
    Payment Gateway

    Payment gateway record is a specific configuration for a `provider`
    """
    __name__ = 'payment_gateway.gateway'

    name = fields.Char(
        'Name', required=True, states=STATES
    )
    journal = fields.Many2One(
        'account.journal', 'Journal', required=True,
        states=STATES,
    )
    account = fields.Many2One('account.account', "Account", required=True,
        domain=[
            ('type', '!=', None),
            ('closed', '!=', True),
            #('id', If(Eval('context', {}).contains('company'), '=', '!='),
            #    Eval('context', {}).get('company', -1)),
            ])
    provider = fields.Selection(
        'get_providers', 'Provider', required=True,
        states=STATES,
    )
    method = fields.Selection(
        'get_methods', 'Method', required=True, states=STATES
    )
    test = fields.Boolean('Test Account', states=STATES)

    users = fields.Many2Many(
        'payment_gateway.gateway-res.user', 'payment_gateway', 'user', 'Users'
    )
    configured = fields.Boolean('Configured ?', readonly=True)

    @classmethod
    def __setup__(cls):
        super(PaymentGateway, cls).__setup__()
        cls._buttons.update({
            'test_gateway_configuration': {
                'readonly': ~Bool(Eval('active')),
            },
        })

    @classmethod
    @ModelView.button
    def test_gateway_configuration(cls, gateways):
        # TODO: make this a really connection test
        for gateway in gateways:
            debit_account = gateway.account
            configured = bool(debit_account
                and not debit_account.party_required)
            gateway.configured = configured
            gateway.save()

    @staticmethod
    def default_provider():
        return 'self'

    @classmethod
    def get_providers(cls):
        """
        Downstream modules can add to the list
        """
        return []

    @fields.depends('provider')
    def get_methods(self):
        """
        Downstream modules can override the method and add entries to this
        """
        return []


class PaymentTransaction(Workflow, ModelSQL, ModelView):
    '''Gateway Transaction'''
    __name__ = 'payment_gateway.transaction'

    uuid = fields.Char('UUID', required=True, readonly=True)
    description = fields.Char(
        'Description', states=READONLY_IF_NOT_DRAFT,
    )
    type = fields.Selection(
        [
            ('charge', 'Charge'),
            ('refund', 'Refund'),
        ], 'Type', required=True,
        states=READONLY_IF_NOT_DRAFT,
    )
    origin = fields.Reference(
        'Origin', selection='get_origin',
        states=READONLY_IF_NOT_DRAFT,
    )
    provider_reference = fields.Char(
        'Provider Reference', readonly=True, states={
            'invisible': Eval('state') == 'draft'
        },
    )
    date = fields.Date(
        'Date', required=True,
        states=READONLY_IF_NOT_DRAFT,
    )
    company = fields.Many2One(
        'company.company', 'Company', required=True,
        states=READONLY_IF_NOT_DRAFT,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
        ],
    )
    party = fields.Many2One(
        'party.party', 'Party', required=True, ondelete='RESTRICT',
        context={
            'company': Eval('company', -1),
            },
        states=READONLY_IF_NOT_DRAFT,
    )
    payment_profile = fields.Many2One(
        'party.payment_profile', 'Payment Profile',
        domain=[
            ('party', '=', Eval('party')),
            ('gateway', '=', Eval('gateway')),
        ],
        ondelete='RESTRICT',
        states=READONLY_IF_NOT_DRAFT,
    )
    address = fields.Many2One(
        'party.address', 'Address', required=True,
        domain=[('party', '=', Eval('party'))],
        states=READONLY_IF_NOT_DRAFT,
        ondelete='RESTRICT'
    )
    amount = Monetary(
        'Amount', currency='currency', digits='currency',
        required=True,
        states=READONLY_IF_NOT_DRAFT,
    )
    currency = fields.Many2One(
        'currency.currency', 'Currency',
        required=True,
        states=READONLY_IF_NOT_DRAFT,
    )
    gateway = fields.Many2One(
        'payment_gateway.gateway', 'Gateway', required=True,
        states=READONLY_IF_NOT_DRAFT, ondelete='RESTRICT',
    )
    provider = fields.Function(
        fields.Char('Provider'), 'get_provider'
    )
    method = fields.Function(
        fields.Char('Payment Gateway Method'), 'get_method'
    )
    move = fields.Many2One(
        'account.move', 'Move', readonly=True, ondelete='RESTRICT'
    )
    logs = fields.One2Many(
        'payment_gateway.transaction.log', 'transaction',
        'Logs', states={
            'readonly': Eval('state') in ('done', 'cancel')
        }
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in-progress', 'In Progress'),
        ('failed', 'Failed'),
        ('authorized', 'Authorized'),
        ('completed', 'Completed'),
        ('posted', 'Posted'),
        ('cancel', 'Canceled'),
    ], 'State', readonly=True)
    shipping_address = fields.Function(
        fields.Many2One('party.address', 'Shipping Address'),
        'get_shipping_address'
    )
    credit_account = fields.Many2One(
        'account.account', 'Credit Account',
        domain=[
            ('company', '=', Eval('company', -1)),
            ('type.receivable', '=', True)
            ],
        states=READONLY_IF_NOT_DRAFT,
        required=True)
    last_four_digits = fields.Char('Last Four Digits')
    charge_id = fields.Char("Charge ID", readonly=True)
    dispute_reason = fields.Char("Dispute Reason", readonly=True,
        states={
            'invisible': ~Eval('dispute_reason'),
            })
    dispute_status = fields.Char("Dispute Status", readonly=True,
        states={
            'invisible': ~Eval('dispute_status'),
            })
    provider_token = fields.Char('Provider Token', readonly=True)
    approval_url = fields.Char('Approval URL', readonly=True)

    @classmethod
    def __setup__(cls):
        super(PaymentTransaction, cls).__setup__()
        cls._order.insert(0, ('date', 'DESC'))

        cls._transitions |= set((
            ('draft', 'in-progress'),
            ('draft', 'authorized'),
            ('draft', 'completed'),     # manual payments
            ('in-progress', 'failed'),
            ('in-progress', 'authorized'),
            ('in-progress', 'completed'),
            ('in-progress', 'cancel'),
            ('authorized', 'cancel'),
            ('authorized', 'completed'),
            ('completed', 'posted'),
            ('draft', 'posted'),       # direct charges for e.g. credit cards
        ))
        cls._buttons.update({
            'process': {
                'invisible': ~(
                    (Eval('state') == 'draft')
                    & (Eval('method') == 'manual')
                    & (Eval('type') == 'charge')
                ),
            },
            'cancel': {
                'invisible': ~Eval('state').in_(['in-progress', 'authorized']),
            },
            'authorize': {
                'invisible': ~(
                    (Eval('state') == 'draft')
                    & Eval('payment_profile', True)
                    & (Eval('method') == 'credit_card')
                    & (Eval('type') == 'charge')
                ),
            },
            'settle': {
                'invisible': ~(
                    (Eval('state') == 'authorized')
                    & (Eval('method') == 'credit_card')
                    & (Eval('type') == 'charge')
                ),
            },
            'retry': {
                'invisible': ~(
                    (Eval('state') == 'failed')
                    & (Eval('type') == 'charge')
                )
            },
            'capture': {
                'invisible': ~(
                    (Eval('state') == 'draft')
                    & (Eval('type') == 'charge')
                ),
            },
            'post': {
                'invisible': ~(
                    (Eval('state') == 'completed')
                    & (Eval('type').in_(['charge', 'refund']))
                )
            },
            'use_card': {
                'invisible': ~(
                    (Eval('state') == 'draft')
                    & ~Bool(Eval('payment_profile'))
                    & (Eval('method') == 'credit_card')
                ),
            },
            'update_status': {
                'invisible': ~Eval('state').in_(['in-progress'])
            },
            'refund': {
                'invisible': ~(
                    (Eval('type') == 'refund')
                    & (Eval('state') == 'draft')
                )
            }
        })

    @staticmethod
    def default_uuid():
        return str(uuid4())

    @staticmethod
    def default_date():
        Date = Pool().get('ir.date')
        return Date.today()

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_currency():
        Company = Pool().get('company.company')
        if Transaction().context.get('company'):
            company = Company(Transaction().context['company'])
            return company.currency.id

    @staticmethod
    def default_state():
        return 'draft'

    @staticmethod
    def default_type():
        return 'charge'

    def get_rec_name(self, name=None):
        """
        Return the most meaningful rec_name
        """
        if self.state == 'draft':
            return self.uuid
        if not self.payment_profile:
            return '%s/%s' % (self.gateway.name, self.provider_reference)
        return '%s/%s' % (
            self.payment_profile.rec_name, self.provider_reference
        )

    @classmethod
    def search_rec_name(cls, name, clause):
        return [
            'OR',
            [('uuid',) + tuple(clause[1:])],
            [('party',) + tuple(clause[1:])],
        ]

    @fields.depends('party')
    def on_change_party(self):
        if self.party:
            receivable = self.party.account_receivable_used
            self.credit_account = receivable and receivable.id or None
            try:
                address = self.party.address_get(type='invoice')
            except AttributeError:
                # account_invoice module is not installed
                pass
            else:
                self.address = address.id
                self.address.rec_name = address.rec_name

    @fields.depends('payment_profile', 'address')
    def on_change_payment_profile(self):
        if self.payment_profile:
            self.address = self.payment_profile.address.id
            self.address.rec_name = self.payment_profile.address.rec_name

    def get_provider(self, name=None):
        """
        Return the gateway provider based on the gateway
        """
        return self.gateway and self.gateway.provider

    def get_method(self, name=None):
        """
        Return the method based on the gateway
        """
        return self.gateway.method

    @fields.depends('gateway')
    def on_change_gateway(self):
        if self.gateway:
            self.provider = self.gateway.provider
            self.method = self.gateway.method

    @fields.depends('gateway')
    def on_change_with_provider(self):
        return self.get_provider()

    def cancel_self(self):
        """
        Method to cancel the given payment.
        """
        if self.method == 'manual' and \
                self.state in ('in-progress', 'authorized'):
            return True
        raise UserError(
            gettext('payment_gateway.no_cancel_in_progress'))

    def get_rec_blurb(self, name):
        locale = Transaction().context.get('language', 'en') or 'en'
        rv = {
            'subtitle': [
                ('Type', self.type),
                ('Date', dates.format_date(
                    self.date, 'short', locale=locale)),
                ('Amount', numbers.format_currency(
                    self.amount, currency=self.currency.code, locale=locale)),
            ],
            'description': ' | '.join(
                [_f for _f in [
                    self.description,
                    self.payment_profile.rec_name,
                    self.party.rec_name
                ] if _f]
            ),
        }
        if self.payment_profile:
            rv['title'] = '%s | %s' % (
                self.payment_profile.rec_name, self.provider_reference
            )
        else:
            rv['title'] = '%s | %s' % (
                self.gateway.name, self.provider_reference
            )
        return rv

    @classmethod
    def _get_origin(cls):
        'Return list of Model names for origin Reference'
        return ['payment_gateway.transaction']

    @classmethod
    def get_origin(cls):
        IrModel = Pool().get('ir.model')
        models = cls._get_origin()
        models = IrModel.search([('model', 'in', models)])
        return [(None, '')] + [(m.model, m.name) for m in models]

    @classmethod
    def copy(cls, records, default=None):
        if default is None:
            default = {}
        default.update({
            'uuid': cls.default_uuid(),
            'provider_reference': None,
            'move': None,
            'logs': None,
            'state': 'draft',
        })
        return super(PaymentTransaction, cls).copy(records, default)

    @classmethod
    @ModelView.button
    @Workflow.transition('cancel')
    def cancel(cls, transactions):
        for transaction in transactions:
            if transaction.type == 'refund':
                continue

            method_name = 'cancel_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(gettext(
                        'payment_gateway.cancellation_not_available',
                        transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button
    @Workflow.transition('in-progress')
    def authorize(cls, transactions):
        for transaction in transactions:
            method_name = 'authorize_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(gettext(
                        'payment_gateway.authorization_not_available',
                        transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button
    @Workflow.transition('completed')
    def process(cls, transactions):
        """
        Process a given transaction.

        Used only for gateways which have manual/offline method - like cash,
        cheque, external payment etc.
        """
        for transaction in transactions:
            if transaction.method != 'manual':
                raise UserError(
                    gettext('payment_gateway.process_only_manual'))
        pass

    @classmethod
    @ModelView.button
    @Workflow.transition('in-progress')
    def retry(cls, transactions):
        for transaction in transactions:
            method_name = 'retry_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(
                    gettext('payment_gateway.retry_not_available',
                    transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button
    @Workflow.transition('completed')
    def settle(cls, transactions):
        for transaction in transactions:
            method_name = 'settle_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(
                    gettext('payment_gateway.settle_not_available',
                    transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button
    @Workflow.transition('in-progress')
    def capture(cls, transactions):
        for transaction in transactions:
            method_name = 'capture_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(
                    gettext('payment_gateway.capture_not_available',
                    transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button
    @Workflow.transition('posted')
    def post(cls, transactions):
        """
        Complete the transactions by creating account moves and post them.

        This method is likely to end in failure if the initial configuration
        of the journal and fiscal periods have not been done. You could
        alternatively use the safe_post instance method to try to post the
        record, but ignore the error silently.
        """
        for transaction in transactions:
            if not transaction.move:
                transaction.get_move()

    @classmethod
    @ModelView.button
    def refund(cls, transactions):
        for transaction in transactions:
            assert transaction.type == 'refund', \
                "Transaction type must be refund"
            method_name = 'refund_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(
                    gettext('payment_gateway.refund_not_available',
                    transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button
    def update_status(cls, transactions):
        """
        Check the status with the payment gateway provider and update the
        status of this transaction accordingly.
        """
        for transaction in transactions:
            method_name = 'update_%s' % transaction.gateway.provider
            if not hasattr(transaction, method_name):
                raise UserError(
                    gettext('payment_gateway.update_status_not_available',
                    transaction.gateway.provider))
            getattr(transaction, method_name)()

    @classmethod
    @ModelView.button_action('payment_gateway.wizard_transaction_use_card')
    def use_card(cls, transactions):
        pass

    def safe_post(self):
        """
        If the initial configuration including defining a period and
        journal is not completed, marking as done could fail. In
        such cases, just mark as in-progress and let the user to
        manually mark as done.

        Failing  would otherwise rollback transaction but its
        not possible to rollback the payment
        """
        count = 0
        while True:
            if count:
                time.sleep(0.002 * (_retry - count))
            try:
                self.post([self])
            except UserError as exc:
                log = 'Could not mark as done\n'
                log += str(exc)
                # Delete the account move if there's one
                # We need to do this because if we post transactions
                # asyncronously using workers, the unwanted move will be
                # committed causing duplicate moves
                move_exists, move_number = self.delete_move_if_exists()
                if move_exists:
                    log += "\nDeleted account move %s" % move_number
                TransactionLog.create([{
                    'transaction': self,
                    'log': log
                }])
            except _TransactionLockError as e:
                if count < _retry:
                    count += 1
                    logger.debug(f"Retry: {count} for {e}")
                    continue
                raise
            break

    def delete_move_if_exists(self):
        """
        Delete the account move if there's one
        """
        Move = Pool().get('account.move')

        move = Move.search([
            ('origin', '=', '%s,%d' % (self.__name__, self.id)),
            ('lines.party', '=', self.party.id),
        ], limit=1)

        if move:
            number = move[0].number
            Move.delete([move[0]])
            return True, number
        return False, None

    def get_move(self, date=None):
        """
        Create the account move for the payment transaction

        :param date: Optional date for the account move
        :return: Active record of the created move
        """
        pool = Pool()
        Period = pool.get('account.period')
        Move = pool.get('account.move')
        Date = pool.get('ir.date')
        Journal = pool.get('account.journal')

        debit_account = self.gateway.account
        date = date or Date.today()

        move_lines = self.get_move_lines(debit_account, date, reverse=True)
        move_lines += self.get_move_lines(self.credit_account, date)

        journal = self.gateway.journal
        period_id = Period.find(self.company.id, date=date)

        move = Move()
        move.journal = journal
        move.period = period_id
        move.date = date
        move.origin = self
        move.company = self.company
        move.lines = move_lines
        move.save()
        Move.post([move])
        journal = Journal(journal.id)
        # Set the move as the move of this transaction
        self.move = move
        self.save()

        return move

    def get_move_lines(self, account, date, reverse=False):
        """
        Return a list of move lines instances for a payment transaction

        :param account: The account used for this move line(s)
        :param reverse: Create the complementary (reverse) entry
        """
        pool = Pool()
        Currency = pool.get('currency.currency')
        Period = pool.get('account.period')
        Move = pool.get('account.move')
        MoveLine = pool.get('account.move.line')

        line = MoveLine()
        if self.currency != self.company.currency:
            with Transaction().set_context(date=date):
                amount = Currency.compute(self.currency,
                    self.amount, self.company.currency)
            line.amount_second_currency = self.amount
            line.second_currency = self.currency
        else:
            amount = self.amount
            line.amount_second_currency = None
            line.second_currency = None
        if reverse:
            if self.type == 'refund':
                line.debit, line.credit = 0, amount
            else:
                line.debit, line.credit = amount, 0
        else:
            if self.type == 'refund':
                line.debit, line.credit = amount, 0
            else:
                line.debit, line.credit = 0, amount
        if line.amount_second_currency:
            line.amount_second_currency = (
                line.amount_second_currency.copy_sign(
                    line.debit - line.credit))
        line.account = account
        if account.party_required:
            line.party = self.party
        line.origin = self
        line.description = self.rec_name
        return [line]

    def get_shipping_address(self, name):
        """
        Returns the shipping address for the transaction.

        The downstream modules can override this to send the
        appropriate address in transaction.
        """
        return None

    def create_refund(self, amount=None):
        assert self.type == 'charge', "Transaction type must be charge"

        refund_transaction, = self.copy([self])

        refund_transaction.type = 'refund'
        amount = amount or self.amount
        refund_transaction.amount = amount * -1
        refund_transaction.origin = self
        refund_transaction.description = gettext(
            'refund_for_transaction',
            name=self.rec_name, uuid=self.uuid)
        refund_transaction.date = self.default_date()
        refund_transaction.save()

        return refund_transaction


class TransactionLog(ModelSQL, ModelView):
    "Transaction Log"
    __name__ = 'payment_gateway.transaction.log'

    timestamp = fields.DateTime('Event Timestamp', readonly=True)
    transaction = fields.Many2One(
        'payment_gateway.transaction', 'Transaction',
        required=True, readonly=True, ondelete='CASCADE',
    )
    is_system_generated = fields.Boolean('Is System Generated')
    log = fields.Text(
        'Log', required=True,
        states={'readonly': Eval('is_system_generated', True)}
    )

    @staticmethod
    def default_is_system_generated():
        return False

    @staticmethod
    def default_timestamp():
        return datetime.now(timezone.utc)

    @classmethod
    def serialize_and_create(cls, transaction, data):
        """
        Serialise a given object and then save it as a log

        :param transaction: The transaction against which the log needs to be
                            saved
        :param data: The data object that needs to be saved
        """
        return cls.create([{
            'transaction': transaction,
            'log': yaml.dump(data, default_flow_style=False),
        }])[0]


WHEN_CP = {
    # Required if card is present
    #'required': Bool(Eval('card_present')),

    # Readonly if card is **not** present
    'readonly': ~Bool(Eval('card_present'))
}
WHEN_CNP = {
    # Required if card is not present
    #'required': ~Bool(Eval('card_present')),

    # Readonly if card is present
    'readonly': Bool(Eval('card_present'))
}


class BaseCreditCardViewMixin(object):
    """
    A Reusable Mixin class to get Credit Card view
    """
    __slots__ = ()

    card_present = fields.Boolean(
        'Card is Present',
        help="If the card is present and the card can be swiped"
    )
    swipe_data = fields.Char(
        'Swipe Card',
        states=WHEN_CP,
    )
    owner = fields.Char(
        'Card Owner',
        states=WHEN_CNP,
    )
    number = fields.Char(
        'Card Number',
        states=WHEN_CNP,
    )
    expiry_month = fields.Selection(
        [
            ('01', '01-January'),
            ('02', '02-February'),
            ('03', '03-March'),
            ('04', '04-April'),
            ('05', '05-May'),
            ('06', '06-June'),
            ('07', '07-July'),
            ('08', '08-August'),
            ('09', '09-September'),
            ('10', '10-October'),
            ('11', '11-November'),
            ('12', '12-December'),
        ], 'Expiry Month',
        states=WHEN_CNP,
    )
    expiry_year = fields.Char(
        'Expiry Year', size=4,
        states=WHEN_CNP,
    )
    csc = fields.Char(
        'Card Security Code (CVV/CVD)', size=4, states=WHEN_CNP,
        help='CVD/CVV/CVN'
    )

    @staticmethod
    def default_owner():
        """
        If a party is provided in the context fill up this instantly
        """
        Party = Pool().get('party.party')

        party_id = Transaction().context.get('party')
        if party_id:
            return Party(party_id).name

    # https://en.wikipedia.org/wiki/Magnetic_stripe_card
    pattern = r'''
    ^%(?P<FC>\w)             # Start with '%', followed by a single alphanumeric character (FC)
    (?P<PAN>\d+)             # Followed by one or more digits (PAN)
    \^(?P<NAME>.{2,26})      # Followed by '^' and 2 to 26 characters for the name (NAME)
    \^(?P<YY>\d{2})          # Followed by '^' and two digits for the year (YY)
    (?P<MM>\d{2})            # Followed by two digits for the month (MM)
    (?P<SC>\d{0,3}|\^)       # Followed by up to three digits or '^' for the security code (SC)
    (?P<DD>.*)               # Followed by any remaining characters (DD)
    \?$
    '''
    track1_re = re.compile(pattern)

    @fields.depends('swipe_data')
    def on_change_swipe_data(self):
        """
        Try to parse the track1 and track2 data into Credit card information
        """
        if not self.swipe_data:
            return
        try:
            track1, track2 = self.swipe_data.split(';')
        except ValueError:
            self.owner = ''
            self.number = ''
            self.expiry_month = ''
            self.expiry_year = ''
        else:
            match = self.track1_re.match(track1)
            if match:
                # Track1 matched, extract info and send
                assert match.group('FC').upper() == 'B', 'Unknown card Format Code'  # noqa

                self.owner = match.group('NAME')
                self.number = match.group('PAN')
                self.expiry_month = match.group('MM')
                self.expiry_year = '20' + match.group('YY')

            # TODO: Match track 2


class PaymentProfile(DeactivableMixin, ModelSQL, ModelView):
    """
    Secure Payment Profile

    Several payment gateway service providers offer a secure way to store
    confidential customer credit card insformation on their server.
    Transactions can then be processed against these profiles without the need
    to recollect payment information from the customer, and without the need
    to store confidential credit card information in Tryton.

    This model represents a profile thus stored with any of the third party
    providers.
    """
    __name__ = 'party.payment_profile'

    sequence = fields.Integer('Sequence', required=True)
    party = fields.Many2One('party.party', 'Party', required=True)
    name = fields.Char('Cardholder name')  # Make required later
    address = fields.Many2One(
        'party.address', 'Address', required=True,
        domain=[('party', '=', Eval('party'))],
    )
    gateway = fields.Many2One(
        'payment_gateway.gateway', 'Gateway', required=True,
        ondelete='RESTRICT', readonly=True,
    )
    provider_reference = fields.Char(
        'Provider Reference', required=True, readonly=True
    )
    last_4_digits = fields.Char('Last 4 digits', readonly=True)
    expiry_month = fields.Selection([
        ('01', '01-January'),
        ('02', '02-February'),
        ('03', '03-March'),
        ('04', '04-April'),
        ('05', '05-May'),
        ('06', '06-June'),
        ('07', '07-July'),
        ('08', '08-August'),
        ('09', '09-September'),
        ('10', '10-October'),
        ('11', '11-November'),
        ('12', '12-December'),
    ], 'Expiry Month', required=True, readonly=True)
    expiry_year = fields.Char(
        'Expiry Year', required=True, size=4, readonly=True
    )

    @staticmethod
    def default_sequence():
        return 10

    @classmethod
    def __setup__(cls):
        super(PaymentProfile, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    def get_rec_name(self, name=None):
        if self.last_4_digits:
            return ' '.join([self.gateway.name, 'xxxx', self.last_4_digits])
        return 'Incomplete Card'


class AddPaymentProfileView(BaseCreditCardViewMixin, ModelView):
    """
    View for adding a payment profile
    """
    __name__ = 'party.payment_profile.add_view'

    party = fields.Many2One(
        'party.party', 'Party', required=True,
    )
    address = fields.Many2One(
        'party.address', 'Address', required=True,
        domain=[('party', '=', Eval('party'))],
    )
    gateway = fields.Many2One(
        'payment_gateway.gateway', 'Gateway', required=True,
        domain=[('method', '!=', 'manual')],
    )


class AddPaymentProfile(Wizard):
    """
    Add a payment profile
    """
    __name__ = 'party.party.payment_profile.add'

    start_state = 'card_info'

    card_info = StateView(
        'party.payment_profile.add_view',
        'payment_gateway.payment_profile_add_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Add', 'add', 'tryton-ok', default=True)
        ]
    )
    add = StateTransition()

    def default_card_info(self, fields):
        Party = Pool().get('party.party')

        party = Party(Transaction().context.get('active_id'))

        res = {
                'party': party.id,
                'owner': party.name,
        }

        try:
            address = self.party.address_get(type='invoice')
        except AttributeError:
            # account_invoice module is not installed
            pass
        else:
            res['address'] = address.id

        return res

    def create_profile(self, provider_reference, **kwargs):
        """
        A helper function that creates a profile from the card information
        that was entered into the View of the wizard. This helper could be
        called by the method which implement the API and wants to create the
        profile with provider_reference.

        :param provider_reference: Value for the provider_reference field.
        :return: Active record of the created profile
        """
        Profile = Pool().get('party.payment_profile')

        profile = Profile(
            name=self.card_info.owner,
            party=self.card_info.party.id,
            address=self.card_info.address.id,
            gateway=self.card_info.gateway.id,
            last_4_digits=self.card_info.number[-4:],
            expiry_month=self.card_info.expiry_month,
            expiry_year=self.card_info.expiry_year,
            provider_reference=provider_reference,
            **kwargs
        )
        profile.save()

        # Wizard session data is stored in database
        # Make sure credit card info does not hit the database
        self.card_info.number = None
        self.card_info.csc = None
        return profile

    def transition_add(self):
        """
        Downstream module implementing the functionality should check for the
        provider type and handle it accordingly.

        To handle, name your method transition_add_<provider_name>. For example
        if your proivder internal name is paypal, then the method name
        should be `transition_add_paypal`

        Once validated, the payment profile must be created by the method and
        the active record of the created payment record should be returned.

        A helper function is provided in this class itself which fills in most
        of the information automatically and the only additional information
        required is the reference from the payment provider.

        If return_profile is set to True in the context, then the created
        profile is returned.
        """
        method_name = 'transition_add_%s' % self.card_info.gateway.provider
        if Transaction().context.get('return_profile'):
            return getattr(self, method_name)()
        else:
            getattr(self, method_name)()
            return 'end'


class TransactionUseCardView(BaseCreditCardViewMixin, ModelView):
    """
    View for putting in credit card information
    """
    __name__ = 'payment_gateway.transaction.use_card.view'


class TransactionUseCard(Wizard):
    """
    Transaction using Credit Card wizard
    """
    __name__ = 'payment_gateway.transaction.use_card'

    start_state = 'card_info'

    card_info = StateView(
        'payment_gateway.transaction.use_card.view',
        'payment_gateway.transaction_use_card_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Authorize', 'authorize', 'tryton-forward'),
            Button('Capture', 'capture', 'tryton-ok', default=True),
        ]
    )
    capture = StateTransition()
    authorize = StateTransition()

    def transition_capture(self):
        """
        Delegates to the capture method for the provider in
        payment_gateway.transaction
        """
        PaymentTransaction = Pool().get('payment_gateway.transaction')

        transaction = PaymentTransaction(
            Transaction().context.get('active_id')
        )

        getattr(transaction, 'capture_%s' % transaction.gateway.provider)(
            self.card_info
        )

        self.clear_cc_info()
        return 'end'

    def transition_authorize(self):
        """
        Delegates to the authorize method for the provider in
        payment_gateway.transaction
        """
        PaymentTransaction = Pool().get('payment_gateway.transaction')

        transaction = PaymentTransaction(
            Transaction().context.get('active_id')
        )

        getattr(transaction, 'authorize_%s' % transaction.gateway.provider)(
            self.card_info
        )

        self.clear_cc_info()
        return 'end'

    def clear_cc_info(self):
        """
        Tryton stores Wizard session data while it's execution
        We need to make sure credit card info does not hit the database
        """
        self.card_info.number = None
        self.card_info.csc = None


class User(metaclass=PoolMeta):
    __name__ = 'res.user'

    payment_gateways = fields.Many2Many(
        'payment_gateway.gateway-res.user', 'user', 'payment_gateway',
        'Payment Gateways'
    )


class PaymentGatewayResUser(ModelSQL):
    'Payment Gateway - Res User'
    __name__ = 'payment_gateway.gateway-res.user'
    _table = 'payment_gateway_gateway_res_user'

    payment_gateway = fields.Many2One(
        'payment_gateway.gateway', 'Payment Gateway', ondelete='CASCADE',
        required=True
    )
    user = fields.Many2One(
        'res.user', 'User', ondelete='RESTRICT', required=True
    )


class AccountMove(metaclass=PoolMeta):
    __name__ = 'account.move'

    @classmethod
    def _get_origin(cls):
        return super()._get_origin() + ['payment_gateway.transaction']


class AccountMoveLine(metaclass=PoolMeta):
    __name__ = 'account.move.line'

    @classmethod
    def _get_origin(cls):
        return super()._get_origin() + ['payment_gateway.transaction']


class CreateRefund(Wizard):
    "Create Refund"
    __name__ = "payment_gateway.transaction.create_refund"
    start_state = 'open'

    open = StateAction('payment_gateway.act_transaction')

    def do_open(self, action):
        GatewayTransaction = Pool().get('payment_gateway.transaction')

        transactions = GatewayTransaction.browse(
            Transaction().context['active_ids']
        )

        refund_transactions = []
        for transaction in transactions:
            refund_transactions.append(transaction.create_refund())

        data = {'res_id': list(map(int, refund_transactions))}
        return action, data

    def transition_open(self):
        return 'end'

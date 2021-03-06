import graphene
from django.core.exceptions import ValidationError

from ....account.models import User
from ....core.permissions import OrderPermissions
from ....order import events, models
from ....order.actions import (
    cancel_order,
    clean_mark_order_as_paid,
    mark_order_as_paid,
    order_captured,
    order_refunded,
    order_voided,
)
from ....order.error_codes import OrderErrorCode
from ....payment import CustomPaymentChoices, PaymentError, TransactionKind, gateway
from ...account.i18n import I18nMixin
from ...account.types import AddressInput
from ...core.mutations import ModelMutation
from ...core.mutations import BaseMutation
from ...core.scalars import Decimal
from ...core.types.common import OrderError
from ...core.utils import validate_required_string_field
from ...order.types import Order, OrderEvent


def clean_order_cancel(order):
    if order and not order.can_cancel():
        raise ValidationError(
            {
                "order": ValidationError(
                    "This order can't be canceled.",
                    code=OrderErrorCode.CANNOT_CANCEL_ORDER,
                )
            }
        )


def clean_payment(payment):
    if not payment:
        raise ValidationError(
            {
                "payment": ValidationError(
                    "There's no payment associated with the order.",
                    code=OrderErrorCode.PAYMENT_MISSING,
                )
            }
        )


def clean_order_capture(payment):
    clean_payment(payment)
    if not payment.is_active:
        raise ValidationError(
            {
                "payment": ValidationError(
                    "Only pre-authorized payments can be captured",
                    code=OrderErrorCode.CAPTURE_INACTIVE_PAYMENT,
                )
            }
        )


def clean_void_payment(payment):
    """Check for payment errors."""
    clean_payment(payment)
    if not payment.is_active:
        raise ValidationError(
            {
                "payment": ValidationError(
                    "Only pre-authorized payments can be voided",
                    code=OrderErrorCode.VOID_INACTIVE_PAYMENT,
                )
            }
        )


def clean_refund_payment(payment):
    clean_payment(payment)
    if payment.gateway == CustomPaymentChoices.MANUAL:
        raise ValidationError(
            {
                "payment": ValidationError(
                    "Manual payments can not be refunded.",
                    code=OrderErrorCode.CANNOT_REFUND,
                )
            }
        )


def try_payment_action(order, user, payment, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except (PaymentError, ValueError) as e:
        message = str(e)
        events.payment_failed_event(
            order=order, user=user, message=message, payment=payment
        )
        raise ValidationError(
            {"payment": ValidationError(message, code=OrderErrorCode.PAYMENT_ERROR)}
        )


class OrderUpdateInput(graphene.InputObjectType):
    billing_address = AddressInput(description="Billing address of the customer.")
    user_email = graphene.String(description="Email address of the customer.")
    shipping_address = AddressInput(description="Shipping address of the customer.")


class OrderUpdate(ModelMutation, I18nMixin):
    class Arguments:
        id = graphene.ID(required=True, description="ID of an order to update.")
        input = OrderUpdateInput(
            required=True, description="Fields required to update an order."
        )

    class Meta:
        description = "Updates an order."
        model = models.Order
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        draft_order_cleaned_input = super().clean_input(info, instance, data)

        # We must to filter out field added by DraftOrderUpdate
        editable_fields = ["billing_address", "user_email"]
        cleaned_input = {}
        for key in draft_order_cleaned_input:
            if key in editable_fields:
                cleaned_input[key] = draft_order_cleaned_input[key]
        return cleaned_input

    @classmethod
    def save(cls, info, instance, cleaned_input):
        super().save(info, instance, cleaned_input)
        if instance.user_email:
            user = User.objects.filter(email=instance.user_email).first()
            instance.user = user
        instance.save()


class OrderAddNoteInput(graphene.InputObjectType):
    message = graphene.String(
        description="Note message.", name="message", required=True
    )


class OrderAddNote(BaseMutation):
    order = graphene.Field(Order, description="Order with the note added.")
    event = graphene.Field(OrderEvent, description="Order note created.")

    class Arguments:
        id = graphene.ID(
            required=True,
            description="ID of the order to add a note for.",
            name="order",
        )
        input = OrderAddNoteInput(
            required=True, description="Fields required to create a note for the order."
        )

    class Meta:
        description = "Adds note to the order."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def clean_input(cls, _info, _instance, data):
        try:
            cleaned_input = validate_required_string_field(data["input"], "message")
        except ValidationError:
            raise ValidationError(
                {
                    "message": ValidationError(
                        "Message can't be empty.", code=OrderErrorCode.REQUIRED,
                    )
                }
            )
        return cleaned_input

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)
        cleaned_input = cls.clean_input(info, order, data)
        event = events.order_note_added_event(
            order=order, user=info.context.user, message=cleaned_input["message"],
        )
        return OrderAddNote(order=order, event=event)


class OrderCancel(BaseMutation):
    order = graphene.Field(Order, description="Canceled order.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of the order to cancel.")

    class Meta:
        description = "Cancel an order."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)
        clean_order_cancel(order)
        cancel_order(order=order, user=info.context.user)
        return OrderCancel(order=order)


class OrderMarkAsPaid(BaseMutation):
    order = graphene.Field(Order, description="Order marked as paid.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of the order to mark paid.")

    class Meta:
        description = "Mark order as manually paid."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def clean_billing_address(cls, instance):
        if not instance.billing_address:
            raise ValidationError(
                "Order billing address is required to mark order as paid.",
                code=OrderErrorCode.BILLING_ADDRESS_NOT_SET,
            )

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)

        cls.clean_billing_address(order)
        try_payment_action(
            order, info.context.user, None, clean_mark_order_as_paid, order
        )

        mark_order_as_paid(order, info.context.user)
        return OrderMarkAsPaid(order=order)


class OrderCapture(BaseMutation):
    order = graphene.Field(Order, description="Captured order.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of the order to capture.")
        amount = Decimal(required=True, description="Amount of money to capture.")

    class Meta:
        description = "Capture an order."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def perform_mutation(cls, _root, info, amount, **data):
        if amount <= 0:
            raise ValidationError(
                {
                    "amount": ValidationError(
                        "Amount should be a positive number.",
                        code=OrderErrorCode.ZERO_QUANTITY,
                    )
                }
            )

        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)
        payment = order.get_last_payment()
        clean_order_capture(payment)

        transaction = try_payment_action(
            order, info.context.user, payment, gateway.capture, payment, amount
        )
        # Confirm that we changed the status to capture. Some payment can receive
        # asynchronous webhook with update status
        if transaction.kind == TransactionKind.CAPTURE:
            order_captured(order, info.context.user, amount, payment)
        return OrderCapture(order=order)


class OrderVoid(BaseMutation):
    order = graphene.Field(Order, description="A voided order.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of the order to void.")

    class Meta:
        description = "Void an order."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)
        payment = order.get_last_payment()
        clean_void_payment(payment)

        transaction = try_payment_action(
            order, info.context.user, payment, gateway.void, payment
        )
        # Confirm that we changed the status to void. Some payment can receive
        # asynchronous webhook with update status
        if transaction.kind == TransactionKind.VOID:
            order_voided(order, info.context.user, payment)
        return OrderVoid(order=order)


class OrderRefund(BaseMutation):
    order = graphene.Field(Order, description="A refunded order.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of the order to refund.")
        amount = Decimal(required=True, description="Amount of money to refund.")

    class Meta:
        description = "Refund an order."
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def perform_mutation(cls, _root, info, amount, **data):
        if amount <= 0:
            raise ValidationError(
                {
                    "amount": ValidationError(
                        "Amount should be a positive number.",
                        code=OrderErrorCode.ZERO_QUANTITY,
                    )
                }
            )

        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)
        payment = order.get_last_payment()
        clean_refund_payment(payment)

        transaction = try_payment_action(
            order, info.context.user, payment, gateway.refund, payment, amount
        )

        # Confirm that we changed the status to refund. Some payment can receive
        # asynchronous webhook with update status
        if transaction.kind == TransactionKind.REFUND:
            order_refunded(order, info.context.user, amount, payment)
        return OrderRefund(order=order)

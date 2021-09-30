import graphene
from ....product import models, emails
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProductError
from ...product.types import Product, ProductQueryUsers, Offers
from ..utils import product_permission
from ...account.enums import CountryCodeEnum


class ProductQueryInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="Order user name .")
    offer = graphene.ID(required=False,  description="Product offer.")
    quantity = graphene.Int(required=True, description="Product quantity.")
    message = graphene.String(required=True, description="Product message.")
    country = CountryCodeEnum(description="Country.")


class ProductQueryCreate(ModelMutation):
    product_query_user = graphene.Field(
        ProductQueryUsers, description="A created product Query."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to add product Query."
        )
        input = ProductQueryInput(
            required=True, description="Fields required to create a product Query."
        )

    class Meta:
        description = "Creates a new product Query."
        model = models.ProductQueryUsers
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(info, product_id, only_type=Product, field="product_id")
        user = info.context.user
        if not models.ProductQueryUsers.objects.filter(seller=product.company, user=info.context.user).exists():
            product_query_user = models.ProductQueryUsers.objects.create(seller=product.company, user=user)
        else:
            product_query_user = models.ProductQueryUsers.objects.filter(seller=product.company, user=user).first()
        product_query = models.ProductQuery.objects.create(product_query_user=product_query_user, product=product)
        cleaned_input = cls.clean_input(info, product_query, data.get("input"))
        product_query = cls.construct_instance(product_query, cleaned_input)
        cls.clean_instance(info, product_query)
        cls.save(info, product_query, cleaned_input)
        emails.send_confirm_order_mail_("order/buyer", user.email, product_query)
        emails.send_confirm_order_mail_("order/seller", product.company.user.email, product_query)
        return ProductQueryCreate(product_query_user=product_query_user)

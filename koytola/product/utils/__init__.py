from typing import TYPE_CHECKING, List
from django.db import transaction

if TYPE_CHECKING:  # flake8: noqa
    from django.db.models.query import QuerySet
    from ..models import Product, Category


@transaction.atomic
def delete_categories(categories_ids: List[str]):
    """Delete categories and perform all necessary actions.

    Set products of deleted categories as unpublished and then delete categories.
    """
    from ..models import Product, Category

    categories = Category.objects.select_for_update().filter(pk__in=categories_ids)
    categories.prefetch_related("products")

    products = Product.objects.none()
    for category in categories:
        products = products | collect_categories_tree_products(category)

    products.update(is_published=False, publication_date=None)
    categories.delete()


def collect_categories_tree_products(category: "Category") -> "QuerySet[Product]":
    """Collect products from all levels in category tree."""
    products = category.products.all()
    descendants = category.get_descendants()
    for descendant in descendants:
        products = products | descendant.products.all()
    return products

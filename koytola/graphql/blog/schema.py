import graphene

from ..core.fields import FilterInputConnectionField
from ..translations.mutations import BlogTranslate
from .bulk_mutations import BlogBulkDelete, BlogBulkPublish
from .filters import BlogFilterInput
from .mutations import (
    BlogCreate,
    BlogDelete,
    BlogUpdate,
    BlogActivate,
    BlogDeactivate,
    BlogPublish,
    BlogUnPublish,
    BlogImageCreate
)
from .resolvers import (
    resolve_blog,
    resolve_blogs,
    resolve_blog_categories,
    resolve_blog_category,
    resolve_blog,
    resolve_blog_image
)
from .sorters import BlogSortingInput
from .types import Blog, BlogCategory, BlogImages


class BlogQueries(graphene.ObjectType):
    blog_category = graphene.Field(
        BlogCategory,
        id=graphene.Argument(graphene.ID, description="ID of the blog."),
        slug=graphene.String(description="The slug of the blog."),
        description="Look up a blog by ID or slug.",
    )
    blog_categories = graphene.List(
        BlogCategory,
        description="Look up a blog by ID or slug.",
    )

    blog = graphene.Field(
        Blog,
        id=graphene.Argument(graphene.ID, description="ID of the blog."),
        slug=graphene.String(description="The slug of the blog."),
        description="Look up a blog by ID or slug.",
    )
    blogs = FilterInputConnectionField(
        Blog,
        sort_by=BlogSortingInput(description="Sort blogs."),
        filter=BlogFilterInput(description="Filtering options for blogs."),
        description="List of the shop's blogs.",
    )

    blog_image = graphene.Field(
        BlogImages,
        id=graphene.Argument(graphene.ID, description="ID of the blog."),
        description="List of the shop's blogs.",
    )

    def resolve_blog_category(self, info, category_id=None, name=None):
        return resolve_blog_category(info, category_id, name)

    def resolve_blog_categories(self, info, query=None, **kwargs):
        return resolve_blog_categories(info, query, **kwargs)

    def resolve_blog(self, info, id=None, slug=None):
        return resolve_blog(info, id, slug)

    def resolve_blog_image(self, info, id=None):
        return resolve_blog_image(info, id)

    def resolve_blogs(self, info, **kwargs):
        return resolve_blogs(info, **kwargs)


class BlogMutations(graphene.ObjectType):
    blog_create = BlogCreate.Field()
    blog_delete = BlogDelete.Field()
    blog_bulk_delete = BlogBulkDelete.Field()
    blog_bulk_publish = BlogBulkPublish.Field()
    blog_update = BlogUpdate.Field()
    blog_translate = BlogTranslate.Field()
    blog_activate = BlogActivate.Field()
    blog_deactivate = BlogDeactivate.Field()
    blog_publish = BlogPublish.Field()
    blog_unpublish = BlogUnPublish.Field()
    blog_image_create = BlogImageCreate.Field()

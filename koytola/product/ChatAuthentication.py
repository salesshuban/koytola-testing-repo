from channels.db import database_sync_to_async
from ..account.models import User
from django.contrib.auth.models import AnonymousUser
import graphene


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class CustomAuthentication:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode().split('&')
        _model, to = graphene.Node.from_global_id(query_string[0].split('to=')[1])
        _model, by = graphene.Node.from_global_id(query_string[1].split('by=')[1])
        scope['to'] = await get_user(int(to))
        scope['by'] = await get_user(int(by))
        return await self.app(scope, receive, send)

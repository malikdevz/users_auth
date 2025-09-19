import graphene
from .types import *
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
from graphql import GraphQLError


class Query(graphene.ObjectType):
	users=graphene.List(UserType)
	user=graphene.Field(UserType, username=graphene.String(required=True))

	@login_required
	def resolve_users(self,info, **kwargs):
		user=info.context.user
		if user.is_superuser:
			return User.objects.all()
		else:
			raise GraphQLError("OPERATION_DENIED")
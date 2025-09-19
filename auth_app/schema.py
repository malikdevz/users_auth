import graphene
from .queries import Query as uQuery
from .mutations import Mutation as uMutation

class Query(uQuery, graphene.ObjectType):
	pass


class Mutation(uMutation, graphene.ObjectType):
	pass



schema=graphene.Schema(query=Query, mutation=Mutation)
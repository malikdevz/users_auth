from django.urls import path
from .views import *
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', Index.as_view(), name="users_welcom"),
    path('api/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

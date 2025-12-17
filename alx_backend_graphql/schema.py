import graphene
from crm.schema import CRMQuery
class Query(graphene.ObjectType):
    hello = graphene.String()
    crm = graphene.Field(CRMQuery)

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

    def resolve_crm(self, info):
        return CRMQuery()


schema = graphene.Schema(query=Query) 

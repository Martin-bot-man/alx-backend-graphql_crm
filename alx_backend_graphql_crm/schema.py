class Query(graphene.ObjectType):
    hello = graphene.String(description='A typical hello')

    def resolve_hello(self, info):
        return 'Hello World'
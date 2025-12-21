import graphene
from graphene_django import DjangoObjectType
from .models import Contact, Deal

class ContactType(DjangoObjectType):
    class Meta:
        model= Contact
        fields='__all__'

class DealType(DjangoObjectType):
    class Meta:
        model= Deal
        fields= '__all__'

class CRMQuery(graphene.objectType):
    all_contacts= graphene.List(ContactType)
    all_deals = graphene.List(DealType)
    contact_by_id= graphene.Field(ContactType, id=graphene.Int(required=True))
    deal_by_id = graphene.Field(DealType, id=graphene.Int(required=True))
    contacts_by_company= graphene.List(ContactType, company=graphene.String(required=True) )
    deals_by_status= graphene.List(DealType, status=graphene.String(required=True))

    def resolve_all_contacts(self, info):
        return Contact.objects.all()
    
    def resolve_all_deals(self, info):
        return Deal.objects.all()
    
    def resolve_contact_by_id(self, info, id):
        try:
            return Contact.objects.get(pk=id)
        except Contact.DoesNotExist:
            return None
        
    def resolve_deal_by_id(self, info, id):
        try:
            return Deal.objects.get(pk=id)
        except Deal.DoesNotExist:
            return None

    def resolve_contacts_by_company(self, info, company):
        return Contact.objects.filter(company=company)

    def resolve_deals_by_status(self, info, status):
        return Deal.objects.filter(status=status)        

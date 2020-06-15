from controlcenter import Dashboard, widgets
from django.db.models import Sum
from django.db.models import Count
from products.models import Product
from groups.models import Group
from agreements.models import Agreement
from members.models import Member
#1
class CoverageLimitsProducts(widgets.SingleBarChart):
    # label and series
    title = 'Coverage limits by Products'

    values_list = ('name', 'coverage_limit')
    # Data source
    #queryset = Product.objects.order_by('-coverage_limit')
    queryset = Product.objects.values('name').annotate(Sum('coverage_limit')).order_by('-coverage_limit')
    #limit_to = 3

class RateByProducts(widgets.SingleBarChart):
    # label and series
    title = 'Rate by Products'

    values_list = ('name', 'price_per_1000_units')
    # Data source
    #queryset = Product.objects.order_by('-coverage_limit')
    queryset = Product.objects.values('name', 'price_per_1000_units').filter()


class MemberByAge(widgets.SingleBarChart):
    # label and series
    title = 'Member By Age'
    model = Member
    values_list = ('name', 'age')
    # Data source
    #queryset = Product.objects.order_by('-coverage_limit')
    queryset = Member.objects.values('name', 'age').filter()


class MemberCountByGroup(widgets.SingleBarChart):
    # label and series
    title = 'Members By Group'
    model = Group
    values_list = ('name', 'number_of_members')
    # Data source
    #queryset = Product.objects.order_by('-coverage_limit')
    queryset = Group.objects.order_by('-number_of_members').annotate(number_of_members=Count('member_set')) # annotate the queryset


class AgreementByProducts(widgets.ItemList):
    # label and series
    title = 'Coverage limits by Agreements and Products'
    model = Product
    list_display = ('name', 'type')

    # Data source
    #queryset = Product.objects.order_by('-coverage_limit').annotate(Sum('coverage_limit'))


#2
class GroupList(widgets.ItemList):
    title = 'Groups by Purpose'
    model = Group
    list_display = ('name', 'purpose', 'group_date')

#3
class AgreementList(widgets.ItemList):
    # This widget displays a list of agreements ordered in the Group
    title = 'Agreements by Group'
    model = Agreement
    list_display = ('name', 'group', 'agreement_date')



class MyDashboard(Dashboard):
    widgets = (
        CoverageLimitsProducts,
        RateByProducts,
        MemberByAge,
        MemberCountByGroup,
        AgreementByProducts,
        GroupList,
        AgreementList,

    )

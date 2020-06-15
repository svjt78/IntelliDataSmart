from controlcenter import Dashboard, widgets
from django.db.models import Sum
from products.models import Product
from groups.models import Group

class MySingleBarChart(widgets.SingleBarChart):
    # label and series
    values_list = ('name', 'coverage_limit')
    # Data source
    #queryset = Product.objects.order_by('-coverage_limit')
    queryset = Product.objects.values('name').annotate(Sum('coverage_limit')).order_by('-coverage_limit')
    #limit_to = 3

class ModelItemList(widgets.ItemList):
    model = Group
    list_display = ('name', 'description')

class AgreementWidget(widgets.ItemList):
    # This widget displays a list of agreements ordered in the Group
    title = 'Agreements in Group'
    model = Agreement
    list_display = ('name', 'group', 'agreement_date')



class MyDashboard(Dashboard):
    widgets = (
        MySingleBarChart,
        ModelItemList,
        AgreementWidget,
    )

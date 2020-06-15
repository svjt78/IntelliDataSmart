import datetime
from django.db.models import Count
from django.utils import timezone
from controlcenter import Dashboard, widgets
from django.db.models import Sum
from products.models import Product
from groups.models import Group
from agreements.models import Agreement

class MenuWidget(widgets.ItemList):
    # This widget displays a list of agreements ordered in the Group
    title = 'Agreements in Group'
    model = Agreement
    list_display = ('name', 'group', 'agreement_date')


class MyDashboard(Dashboard):
    widgets = (
        MenuWidget,
    )

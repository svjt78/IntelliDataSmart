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
    list_display = ['name', 'ocount']
    list_display_links = ['name']
    # By default ItemList limits queryset to 10 items, but we need all of them
    limit_to = None
    # Sets widget's max-height to 300 px and makes it scrollable
    height = 300

    def get_queryset(self):
        agreements = super(MenuWidget, self).get_queryset().filter()
        today = timezone.now().date()
        return (agreements.product
                .filter(product_set__product_date__lte=today, name='ciao')
                .order_by('-ocount')
                .annotate(ocount=Count('product_set')))


class MyDashboard(Dashboard):
    widgets = (
        MenuWidget,
    )

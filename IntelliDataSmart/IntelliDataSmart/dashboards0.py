from controlcenter import Dashboard, widgets
from groups.models import Group

class ModelItemList(widgets.ItemList):
    model = Group
    list_display = ('pk', 'name')

class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )

from django.conf.urls import url

from . import views

app_name = 'groups'

urlpatterns = [
    url(r"^$", views.ListGroups.as_view(), name="all"),
    url(r"^new/$", views.CreateGroup.as_view(), name="create"),
    url(r"^search/$", views.SearchGroupsForm, name="search"),
    url(r"^search/results/$", views.SearchGroupsList.as_view(), name="search_results"),
    url(r"^posts/in/(?P<pk>\d+)/$",views.SingleGroup.as_view(),name="single"),
    url(r"^update/(?P<pk>\d+)/$",views.UpdateGroup.as_view(),name="update"),
    url(r"^delete/(?P<pk>\d+)/$",views.DeleteGroup.as_view(),name="delete"),
    url(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),
]

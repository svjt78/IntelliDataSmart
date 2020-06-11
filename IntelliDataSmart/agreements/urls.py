from django.conf.urls import url

from . import views

app_name = 'agreements'

urlpatterns = [
    url(r"^$", views.ListAgreements.as_view(), name="all"),
    url(r"^new/$", views.CreateAgreement.as_view(), name="create"),
    url(r"^search/$", views.SearchAgreementsForm, name="search"),
    url(r"^(?P<pk>\d+)/contracts/show/$", views.ShowContractsList.as_view(), name="show_contracts"),
    url(r"^search/results/$", views.SearchAgreementsList.as_view(), name="search_results"),
    url(r"^posts/in/(?P<pk>\d+)/$",views.SingleAgreement.as_view(),name="single"),
    url(r"^update/(?P<pk>\d+)/$",views.UpdateAgreement.as_view(),name="update"),
    url(r"^delete/(?P<pk>\d+)/$",views.DeleteAgreement.as_view(),name="delete"),
    ]

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
import time
from django.db.models import Q
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from django.db.models import Count
from . import models
from . import forms
from groups.models import Group,GroupMember
from members.models import Member
from agreements.models import Agreement
from products.models import Product

class SingleAgreement(generic.DetailView):
    context_object_name = 'agreement_details'
    model = models.Agreement
    template_name = 'agreements/agreement_detail.html'

class ListAgreements(generic.ListView):
    model = models.Agreement
    template_name = 'agreements/agreement_list.html'
    #form_class = forms.GroupForm

    def get_queryset(self):
        return Agreement.objects.all()


class CreateAgreement(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'agreements.add_agreement'
    login_url = '/login/'
    context_object_name = 'agreement_details'
    redirect_field_name = 'agreements/agreement_list.html'
    form_class = forms.AgreementForm
    model = models.Agreement
    template_name = 'agreements/agreement_form.html'

    def dispatch(self, request, *args, **kwargs):

        """
        Overridden so we can make sure the `Group` instance exists
        before going any further.
        """
        self.group = get_object_or_404(models.Group, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        if not self.request.user.has_perm('agreements.add_agreement'):
            raise HttpResponseForbidden()
        else:
            """
            Overridden to add the group relation to the `Member` instance.
            """
            form.instance.group = self.group
            form.instance.creator = self.request.user
            return super().form_valid(form)


@permission_required("agreements.add_agreement")
def VersionAgreement(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(Agreement, pk = pk)

    # pass the object as instance in form
    form = forms.AgreementForm(request.POST or None, instance = obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
            obj.pk = int(round(time.time() * 1000))
            form.save()
            return HttpResponseRedirect(reverse("agreements:all"))

    else:

            # add form dictionary to context
            context["form"] = form

            return render(request, "agreements/agreement_form.html", context)



class UpdateAgreement(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'agreements.change_agreement'
    login_url = '/login/'
    context_object_name = 'agreement_details'
    redirect_field_name = 'agreements/agreement_detail.html'
    form_class = forms.AgreementForm
    model = models.Agreement
    template_name = 'agreements/agreement_form.html'

    def form_valid(self, form):

        if not self.request.user.has_perm('agreements.change_agreement'):
            raise HttpResponseForbidden()
        else:
            return super().form_valid(form)


class DeleteAgreement(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
#    fields = ("name", "description")
    permission_required = 'agreements.delete_agreement'
    login_url = '/login/'
    context_object_name = 'agreement_details'
    form_class = forms.AgreementForm
    model = models.Agreement
    template_name = 'agreements/agreement_delete_confirm.html'
    success_url = reverse_lazy("agreements:all")

    def form_valid(self, form):

        if not self.request.user.has_perm('agreements.delete_agreement'):
            raise HttpResponseForbidden()
        else:
            return super().form_valid(form)


def SearchAgreementsForm(request):
    return render(request,'agreements/agreement_search_form.html')


class SearchAgreementsList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Agreement
    template_name = 'agreements/agreement_search_list.html'

    def get_queryset(self, **kwargs): # new
        query = self.request.GET.get('q', None)
        object_list = Agreement.objects.filter(
            Q(pk__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query)
        )
        return object_list


class ShowAgreementsProductsList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Agreement
    template_name = 'agreements/agreement_products_list.html'

    def get_queryset(self): # new
        agreement = get_object_or_404(models.Agreement, pk=self.kwargs['pk'])
        object_list = agreement.product.all()

        return object_list


class ShowContractsList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Agreement
    template_name = 'agreements/agreement_list.html'

    def get_queryset(self): # new
        group = get_object_or_404(models.Agreement, pk=self.kwargs['pk'])
        object_list = agreement.contract_set.all()

        return object_list

class ShowAgreementsProductsList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Agreement
    template_name = 'products/product_list.html'

    def get_queryset(self): # new
        agreement = get_object_or_404(models.Agreement, pk=self.kwargs['pk'])
        object_list = agreement.product.all()

        return object_list

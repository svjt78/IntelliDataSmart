from django.contrib import messages
from django.shortcuts import render
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


class CreateAgreement(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    context_object_name = 'agreement_details'
    redirect_field_name = 'agreements/agreement_list.html'
    form_class = forms.AgreementForm
    model = models.Agreement
    template_name = 'agreements/agreement_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user

        return super().form_valid(form)


class UpdateAgreement(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    context_object_name = 'agreement_details'
    redirect_field_name = 'agreements/agreement_detail.html'
    form_class = forms.AgreementForm
    model = models.Agreement
    template_name = 'agreements/agreement_form.html'



class DeleteAgreement(LoginRequiredMixin, generic.DeleteView):
#    fields = ("name", "description")
    login_url = '/login/'
    context_object_name = 'agreement_details'
    form_class = forms.AgreementForm
    model = models.Agreement
    template_name = 'agreements/agreement_delete_confirm.html'
    success_url = reverse_lazy("agreements:all")


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


class ShowContractsList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = Agreement
    template_name = 'agreements/agreement_list.html'

    def get_queryset(self): # new
        group = get_object_or_404(models.Agreement, pk=self.kwargs['pk'])
        object_list = agreement.contract_set.all()

        return object_list

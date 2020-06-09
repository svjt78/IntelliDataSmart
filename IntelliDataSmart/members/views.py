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
from groups.models import Group
from . import models
from . import forms


class SingleMember(generic.DetailView):
    context_object_name = 'member_details'
    model = models.Member
    template_name = 'members/member_detail.html'
    #form_class = forms.MemberForm

class ListMembers(generic.ListView):
    context_object_name = 'member_list'
    model = models.Member
    template_name = 'members/member_list.html'

    #form_class = forms.MemberForm

    def get_queryset(self):
    #    return Member.objects.filter(group=group_name)
    #    return Member.objects.all
        return models.Member.objects.prefetch_related('group')

class CreateMember(LoginRequiredMixin, generic.CreateView):
    #fields = ("name", "age")
    login_url = '/login/'
    template_name = 'members/member_form.html'
    context_object_name = 'member_details'
    redirect_field_name = 'members/member_detail.html'
    model = models.Member
    form_class = forms.MemberForm

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Group` instance exists
        before going any further.
        """
        self.group = get_object_or_404(models.Group, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overridden to add the group relation to the `Member` instance.
        """
        form.instance.group = self.group
        return super().form_valid(form)



class UpdateMember(LoginRequiredMixin, generic.UpdateView):
    #fields = ("name", "age")
    login_url = '/login/'
    template_name = 'members/member_form.html'
    #context_object_name = 'member_details'
    redirect_field_name = 'members/member_detail.html'
    model = models.Member
    form_class = forms.MemberForm


class DeleteMember(LoginRequiredMixin, generic.DeleteView,):
    login_url = '/login/'
    context_object_name = 'member_details'
    form_class = forms.MemberForm
    model = models.Member
    template_name = 'members/member_delete_confirm.html'
    success_url = reverse_lazy("members:all")


    def delete(self, *args, **kwargs):
        messages.success(self.request, "Member Deleted")
        return super().delete(*args, **kwargs)

def SearchMembersForm(request):
    return render(request,'members/member_search_form.html')


class SearchMembersList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = models.Member
    template_name = 'members/member_search_list.html'

    def get_queryset(self, **kwargs): # new
        query = self.request.GET.get('q', None)
        object_list = models.Member.objects.filter(
            Q(name__icontains=query) | Q(age__icontains=query)
        )
        return object_list

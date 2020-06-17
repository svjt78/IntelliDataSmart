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
from groups.models import Group
from members.models import Member
from . import models
from . import forms
from members.forms import MemberForm


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

class CreateMember(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #fields = ("name", "age")
    permission_required = 'members.add_member'
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

        if not self.request.user.has_perm('members.add_member'):
            raise HttpResponseForbidden()
        else:
            """
            Overridden to add the group relation to the `Member` instance.
            """
            form.instance.group = self.group
            form.instance.creator = self.request.user
            return super().form_valid(form)


@permission_required("members.add_member")
def VersionMember(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(Member, pk = pk)

    # pass the object as instance in form
    form = MemberForm(request.POST or None, instance = obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
            obj.pk = int(round(time.time() * 1000))
            form.save()
            return HttpResponseRedirect(reverse("members:all"))

    else:

            # add form dictionary to context
            context["form"] = form

            return render(request, "members/member_form.html", context)


class UpdateMember(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    #fields = ("name", "age")
    permission_required = 'members.change_member'
    login_url = '/login/'
    template_name = 'members/member_form.html'
    #context_object_name = 'member_details'
    redirect_field_name = 'members/member_detail.html'
    model = models.Member
    form_class = forms.MemberForm

    def form_valid(self, form):

        if not self.request.user.has_perm('members.change_member'):
            raise HttpResponseForbidden()
        else:
            return super().form_valid(form)


class DeleteMember(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView,):
    permission_required = 'members.delete_member'
    login_url = '/login/'
    context_object_name = 'member_details'
    form_class = forms.MemberForm
    model = models.Member
    template_name = 'members/member_delete_confirm.html'
    success_url = reverse_lazy("members:all")


    def delete(self, *args, **kwargs):
        messages.success(self.request, "Member Deleted")
        return super().delete(*args, **kwargs)

    def form_valid(self, form):

        if not self.request.user.has_perm('members.delete_member'):
            raise HttpResponseForbidden()
        else:
            return super().form_valid(form)


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

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required, login_required
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
from groups.models import Group
from members.models import Member
from products.models import Product
from . import models
from . import forms
from products.forms import ProductForm


class SingleProduct(LoginRequiredMixin, generic.DetailView):
    context_object_name = 'product_details'
    model = models.Product
    template_name = 'products/product_detail.html'

class ListProducts(LoginRequiredMixin, generic.ListView):
    model = models.Product
    template_name = 'products/product_list.html'

    def get_queryset(self):
        return models.Product.objects.all()


class CreateProduct(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
#    fields = ("name", "description")
    permission_required = 'products.add_product'
    context_object_name = 'product_details'
    redirect_field_name = 'products/product_list.html'
    form_class = forms.ProductForm
    model = models.Product
    template_name = 'products/product_form.html'

    def form_valid(self, form):
        if not self.request.user.has_perm('products.add_product'):
            raise HttpResponseForbidden()
        else:
            form.instance.creator = self.request.user

            return super().form_valid(form)


@permission_required("products.add_product")
@login_required
def VersionProduct(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(Product, pk = pk)

    # pass the object as instance in form
    form = ProductForm(request.POST or None, instance = obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
            obj.pk = int(round(time.time() * 1000))
            form.instance.creator = self.request.user
            form.save()
            return HttpResponseRedirect(reverse("products:all"))

    else:

            # add form dictionary to context
            context["form"] = form

            return render(request, "products/product_form.html", context)


class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'products.change_product'
    context_object_name = 'product_details'
    redirect_field_name = 'products/product_detail.html'
    form_class = forms.ProductForm
    model = models.Product
    template_name = 'products/product_form.html'

    def form_valid(self, form):

        if not self.request.user.has_perm('products.change_product'):
            raise HttpResponseForbidden()
        else:
            form.instance.creator = self.request.user
            return super().form_valid(form)



class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'products.delete_product'
    context_object_name = 'product_details'
    form_class = forms.ProductForm
    model = models.Product
    template_name = 'products/product_delete_confirm.html'
    success_url = reverse_lazy("products:all")

    def form_valid(self, form):

        if not self.request.user.has_perm('products.delete_product'):
            raise HttpResponseForbidden()
        else:
            form.instance.creator = self.request.user
            return super().form_valid(form)


@login_required
def SearchProductsForm(request):
    return render(request,'products/product_search_form.html')


class SearchProductsList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = models.Product
    template_name = 'products/product_search_list.html'

    def get_queryset(self, **kwargs): # new
        query = self.request.GET.get('q', None)
        object_list = Product.objects.filter(
            Q(pk__icontains=query) | Q(name__icontains=query) | Q(type__icontains=query) | Q(description__icontains=query)
        )
        return object_list

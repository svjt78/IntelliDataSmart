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
from groups.models import Group
from members.models import Member
from products.models import Product
from . import models
from . import forms


class SingleProduct(generic.DetailView):
    context_object_name = 'product_details'
    model = models.Product
    template_name = 'products/product_detail.html'

class ListProducts(generic.ListView):
    model = models.Product
    template_name = 'products/product_list.html'

    def get_queryset(self):
        return models.Product.objects.all()


class CreateProduct(LoginRequiredMixin, generic.CreateView):
#    fields = ("name", "description")
    login_url = '/login/'
    context_object_name = 'product_details'
    redirect_field_name = 'products/product_list.html'
    form_class = forms.ProductForm
    model = models.Product
    template_name = 'products/product_form.html'


class UpdateProduct(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    context_object_name = 'product_details'
    redirect_field_name = 'products/product_detail.html'
    form_class = forms.ProductForm
    model = models.Product
    template_name = 'products/product_form.html'


class DeleteProduct(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    context_object_name = 'product_details'
    form_class = forms.ProductForm
    model = models.Product
    template_name = 'products/product_delete_confirm.html'
    success_url = reverse_lazy("products:all")


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

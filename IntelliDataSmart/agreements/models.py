from datetime import datetime
from django.conf import settings
import uuid
from datetime import datetime
from pytz import timezone
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from groups.utils import create_new_ref_number
from groups.models import Group
from products.models import Product
# from accounts.models import User

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()



class Agreement(models.Model):
    agreementid = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    agreement_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="group_set")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="agreements_products_set")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if (self.agreementid == None):
            var = str(uuid.uuid4())
            self.agreementid = var[26:36]

        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("agreements:single", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-agreement_date"]
        #unique_together = ("name", "purpose")

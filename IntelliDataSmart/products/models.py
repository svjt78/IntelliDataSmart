from django.conf import settings
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()

class Product(models.Model):
    productid = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

    CHOOSE = 'Unknown Type'
    LIFE = 'LIFE'
    STD = 'STD'
    LTD = 'LTD'
    CI = 'CI'
    PRODUCT_CHOICES = (
        (CHOOSE, 'Unknown Type'),
        (LIFE, 'Life Insurance'),
        (STD, 'Short Term Disability'),
        (LTD, 'Long Term Disability'),
        (CI, 'Critical Illness'),
    )
    type = models.CharField(max_length=100,
                                      choices=PRODUCT_CHOICES,
                                      default=CHOOSE)

    slug = models.SlugField(allow_unicode=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    #coverage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_1000_units = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:single", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-product_date"]
        unique_together = ("name", "type", "product_date")

from django.conf import settings
import datetime
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
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    coverage_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    agreement_date = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, related_name="group_set")
    product = models.ForeignKey(Product,related_name="product_set")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        #agreement_date = datetime.datetime.now().date()
        agreement_date = datetime.datetime.now(tz=EST5EDT())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("agreements:single", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-pk"]
        #unique_together = ("name", "purpose")

class EST5EDT(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)        #2nd Sunday in March
        self.dston = d + datetime.timedelta(days=6-d.weekday())
        d = datetime.datetime(dt.year, 11, 1)       #1st Sunday in Nov
        self.dstoff = d + datetime.timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'


####

####

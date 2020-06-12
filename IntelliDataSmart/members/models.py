from django.conf import settings
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from groups.models import Group
# from accounts.models import User

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()

class Member(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(allow_unicode=True)
    age = models.PositiveIntegerField()

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="member_set")

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    member_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
    #    self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("members:single", kwargs={"pk": self.pk})


    class Meta:
        ordering = ["-member_date"]
        #unique_together = ["name", "group"]

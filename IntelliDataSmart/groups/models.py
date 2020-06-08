from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
# from accounts.models import User

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()



class Group(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    purpose = models.CharField(max_length=255, null=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "purpose")


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships")
    user = models.ForeignKey(User,related_name='identity')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user")

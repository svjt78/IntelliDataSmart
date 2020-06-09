from django.conf import settings
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
    #group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, related_name="association")
    group = models.ForeignKey(Group, null=True, blank=True, related_name="member_set")
    #user = models.ForeignKey(User,related_name='userID')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
    #    self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("members:single", kwargs={"pk": self.pk})


    class Meta:
        ordering = ["pk"]
        #unique_together = ["name", "group"]

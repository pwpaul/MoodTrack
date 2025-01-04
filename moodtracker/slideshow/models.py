from django.db import models


class Slide(models.Model):
    image = models.ImageField(upload_to="slides/")
    caption = models.CharField(max_length=255, null=True, blank=True)

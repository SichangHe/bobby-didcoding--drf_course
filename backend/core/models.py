from django.db import models
from django_extensions.db.models import (ActivatorModel, TimeStampedModel,
                                         TitleDescriptionModel)


class Contact(TimeStampedModel, ActivatorModel, TitleDescriptionModel, models.Model):
    class Meta:
        verbose_name_plural = "Contacts"

    email = models.EmailField(verbose_name="Email")

    def __str__(self) -> str:
        return f"{self.title}"

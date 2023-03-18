from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)


class Item(TimeStampedModel, ActivatorModel, TitleSlugDescriptionModel, models.Model):
    """An item for the shop."""

    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["id"]

    def amount(self):
        return self.price / 100

    def manage_stock(self, quantity):
        self.stock -= int(quantity)
        self.save

    def check_stock(self, quantity):
        return int(quantity) <= self.stock

    def plac_order(self, user, quantity):
        if not self.check_stock(quantity):
            return None
        order: Order = Order.objects.create(user=user, item=self, quantity=quantity)
        self.manage_stock(quantity)
        return order

    def __str__(self) -> str:
        return self.title


class Order(TimeStampedModel, ActivatorModel, models.Model):
    """A single order entry for the shop."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.item.title}"

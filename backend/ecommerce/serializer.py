from collections import OrderedDict

from ecommerce.models import Item, Order
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework_json_api import serializers


class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "There is not enough stock"
    default_code = "invalid"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("title", "stock", "price")


class OrderSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=False)

    class Meta:
        model = Order
        fields = ("item", "quantity")

    def validate(self, result: OrderedDict):
        """Validate `Item` stock level. Raise `NotEnoughStockException` if invalid."""
        item: Item = result.get("item")  # type: ignore
        quantity = result.get("quantity")
        if item.check_stock(quantity):
            return result
        raise NotEnoughStockException

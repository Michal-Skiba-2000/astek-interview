from rest_framework.serializers import ModelSerializer

from menu.models import Dish, Menu


class DishSerializer(ModelSerializer):
    """Serializer for Dish model"""

    class Meta:
        """Meta class for serializer"""
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'preparation_time_in_minutes',
                  'created', 'updated', 'is_vegetarian']


class MenuSerializer(ModelSerializer):
    """Serializer for Menu model"""
    dishes = DishSerializer(read_only=True, many=True)

    class Meta:
        """Meta class for serializer"""
        model = Menu
        fields = ['id', 'name', 'description', 'created', 'updated', 'dishes']

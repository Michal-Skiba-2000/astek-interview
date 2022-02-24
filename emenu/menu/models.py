from django.db import models


class Dish(models.Model):
    """Dish model"""
    name = models.fields.CharField(max_length=32)
    description = models.fields.CharField(max_length=512)
    price = models.fields.DecimalField(max_digits=7, decimal_places=2)
    preparation_time_in_minutes = models.IntegerField()
    created = models.fields.DateTimeField(auto_now_add=True)
    updated = models.fields.DateTimeField(auto_now=True)
    is_vegetarian = models.fields.BooleanField()

    class Meta:
        """Meta info for dish model"""
        verbose_name_plural = "Dishes"

    def __str__(self) -> str:
        """__str__"""
        return str(self.name)


class Menu(models.Model):
    """Menu model"""
    name = models.fields.CharField(max_length=32, unique=True)
    description = models.fields.CharField(max_length=512)
    created = models.fields.DateTimeField(auto_now_add=True)
    updated = models.fields.DateTimeField(auto_now=True)
    dishes = models.ManyToManyField(Dish, related_name='menus')

    def __str__(self) -> str:
        """__str__"""
        return str(self.name)

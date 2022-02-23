from django.db import models


class Menu(models.Model):
    """Menu model"""
    name = models.fields.CharField(max_length=32, unique=True)
    description = models.fields.CharField(max_length=512)
    created = models.fields.DateTimeField(auto_now_add=True)
    updated = models.fields.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """__str__"""
        return str(self.name)


class Dish(models.Model):
    """Dish model"""
    name = models.fields.CharField(max_length=32)
    description = models.fields.CharField(max_length=512)
    price = models.fields.DecimalField(max_digits=7, decimal_places=2)
    preparation_time_in_minutes = models.IntegerField()
    created = models.fields.DateTimeField(auto_now_add=True)
    updated = models.fields.DateTimeField(auto_now=True)
    is_vegetarian = models.fields.BooleanField()
    menus = models.ManyToManyField(Menu, related_name='dishes')

    class Meta:
        """Meta info for dish model"""
        verbose_name_plural = "Dishes"

    def __str__(self) -> str:
        """__str__"""
        return str(self.name)

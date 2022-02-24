from django.db import migrations

from menu.models import Menu, Dish


class Migration(migrations.Migration):
    """Migration that creates initial data for Menu and Dish model"""

    dependencies = [
        ('menu', '0001_initial'),
    ]

    @staticmethod
    def generate_data(apps, schema_editor):
        """Generates initial data for Menu and Dish model"""
        spaghetti = Dish(
            name="Spaghetti",
            description="Napoli spaghetti with tomatoes sauce and pork meat",
            price=25.00,
            preparation_time_in_minutes=15,
            is_vegetarian=False
        )
        spaghetti.save()
        spaghetti_wro = Dish(
            name="Wroclaw Chef Special Spaghetti",
            description="Wroclaw Chef Special Spaghetti",
            price=35.00,
            preparation_time_in_minutes=30,
            is_vegetarian=False
        )
        spaghetti_wro.save()
        spaghetti_krk = Dish(
            name="Krakow Chef Special Spaghetti",
            description="Krakow Chef Special Spaghetti",
            price=40.00,
            preparation_time_in_minutes=20,
            is_vegetarian=True
        )
        spaghetti_krk.save()
        margherita = Dish(
            name="Margherita",
            description="Cheese, tomatoes sauce, ham",
            price=18.00,
            preparation_time_in_minutes=20,
            is_vegetarian=False
        )
        margherita.save()
        barbecue = Dish(
            name="Pizza Barbecue",
            description="Cheese, tomatoes sauce, ham, mushrooms, bbq sauce, chicken",
            price=26.00,
            preparation_time_in_minutes=20,
            is_vegetarian=False
        )
        barbecue.save()

        grande_restaurant_wro_menu = Menu(
            name="Grande Restaurant Wroclaw Menu",
            description="Menu for Grande Restaurant Wroclaw"
        )
        grande_restaurant_wro_menu.save()
        grande_restaurant_wro_menu.dishes.add(spaghetti, spaghetti_wro)
        grande_restaurant_krk_menu = Menu(
            name="Grande Restaurant Krakow Menu",
            description="Menu for Grande Restaurant Krakow"
        )
        grande_restaurant_krk_menu.save()
        grande_restaurant_krk_menu.dishes.add(spaghetti, spaghetti_krk)
        pizza_express_menu = Menu(
            name="Pizza Express Menu",
            description="Menu for Pizza Express"
        )
        pizza_express_menu.save()
        pizza_express_menu.dishes.add(margherita, barbecue)

    operations = [
        migrations.RunPython(generate_data),
    ]

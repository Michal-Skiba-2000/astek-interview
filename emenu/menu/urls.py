from django.urls import path

from menu.views import DishView, MenuView


app_name = 'menu'  # pylint: disable=invalid-name

urlpatterns = [
    path('', MenuView.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>', MenuView.as_view({'put': 'update', 'delete': 'destroy'})),
    path('dish', DishView.as_view({'get': 'list', 'post': 'create'})),
    path('dish/<int:pk>', DishView.as_view({'put': 'update', 'delete': 'destroy'})),
]

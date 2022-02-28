from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from menu.filters import MenuFilterSet
from menu.models import Dish, Menu
from menu.serializers import DishSerializer, MenuSerializer


class MenuView(ModelViewSet):
    """View that implements CRUD for Menu model"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'dishes_number']
    filterset_class = MenuFilterSet

    def list(self, request):
        """Return listed menus"""
        not_empty_menu_queryset = self.get_queryset().annotate(dishes_number=Count('dishes'))\
                                                     .filter(dishes_number__gt=0)
        queryset = self.filter_queryset(not_empty_menu_queryset)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Creates menu by request body data"""
        try:
            menu = Menu(name=request.data['name'], description=request.data['description'])
            menu.save()
            if request.data.get('dishes'):
                menu.dishes.set(*request.data['dishes'])
            return Response(status=201)
        except KeyError:
            return Response(status=400)

    def update(self, request, pk):
        """Updates menu by request body data and url pk"""
        try:
            menu = Menu.objects.filter(pk=pk)
            menu.update(name=request.data['name'], description=request.data['description'])
            if request.data.get('dishes'):
                menu = menu.first()
                menu.dishes.set(request.data['dishes'])
            return Response(status=204)
        except KeyError:
            return Response(status=400)

    def destroy(self, request, pk):
        """Deletes menu by url pk"""
        Menu.objects.filter(pk=pk).delete()
        return Response(status=204)


class DishView(ModelViewSet):
    """View that implements CRUD for Dish model"""
    queryset = Dish.objects.all
    serializer_class = DishSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Return listed dishes"""
        serializer = self.serializer_class(self.queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        """Creates dish by request body data"""
        try:
            Dish.objects.create(**request.data)
            return Response(status=200)
        except KeyError:
            return Response(status=400)

    def update(self, request, pk):
        """Updates dish by request body data and url pk"""
        try:
            Dish.objects.filter(pk=pk).update(**request.data)
            return Response(status=200)
        except KeyError:
            return Response(status=400)

    def destroy(self, request, pk):
        """Deletes dish by url pk"""
        Dish.objects.filter(pk=pk).delete()
        return Response(status=200)

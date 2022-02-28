import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from menu.models import Menu


class TestMenuView(APITestCase):
    TEST_SU_NAME = 'test_admin'
    TEST_SU_EMAIL = 'test_admin@example.com'
    TEST_SU_PASSWORD = 'test_admin'

    def setUp(self) -> None:
        self.client = APIClient()
        superuser = User.objects.create_superuser(
            username=self.TEST_SU_NAME,
            email=self.TEST_SU_EMAIL,
            password=self.TEST_SU_PASSWORD)

        superuser.save()

    def test_list(self) -> None:
        """Test list function without any parameters"""
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode('utf-8'))
        number_of_menus = Menu.objects.all().count()
        self.assertEqual(len(response_data), number_of_menus)

    def test_list_sorting(self) -> None:
        """Test list function with sorting parameter"""
        response_sorted_by_name_asc = self.client.get('/menu/?ordering=name')
        response_sorted_by_name_desc = self.client.get('/menu/?ordering=-name')
        self.assertEqual(response_sorted_by_name_asc.status_code, status.HTTP_200_OK)
        self.assertEqual(response_sorted_by_name_desc.status_code, status.HTTP_200_OK)

        response_sorted_by_name_asc_data = json.loads(response_sorted_by_name_asc.content.decode('utf-8'))
        response_sorted_by_name_desc_data = json.loads(response_sorted_by_name_desc.content.decode('utf-8'))
        self.assertEqual(len(response_sorted_by_name_asc_data), len(response_sorted_by_name_desc_data))

        self.assertEqual(response_sorted_by_name_asc_data, list(reversed(response_sorted_by_name_desc_data)))

    def test_list_filtering(self) -> None:
        """Test list function with filtering parameter"""
        tests_data = [
            {
                'path': '/menu/?name=Grande',
                'expected_length': 2,
            },
            {
                'path': '/menu/?name=Pizza',
                'expected_length': 1,
            },
        ]

        for test_data in tests_data:
            response = self.client.get(test_data['path'])
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = json.loads(response.content.decode('utf-8'))
            self.assertEqual(len(response_data), test_data['expected_length'])

    def test_create_success(self) -> None:
        """Test that checks success scenario for creating menu"""
        initial_number_of_menus = Menu.objects.all().count()
        self.client.login(username=self.TEST_SU_NAME, password=self.TEST_SU_PASSWORD)
        request_data = {'name': 'new menu', 'description': 'new menu description'}
        response = self.client.post('/menu/', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_number_of_menus = Menu.objects.all().count()
        number_of_menus_created = final_number_of_menus-initial_number_of_menus
        self.assertEqual(number_of_menus_created, 1)
        self.client.logout()

    def test_create_failure(self) -> None:
        """Test that checks failure scenario for creating menu"""
        initial_number_of_menus = Menu.objects.all().count()
        self.client.login(username=self.TEST_SU_NAME, password=self.TEST_SU_PASSWORD)
        request_data = {'name': 'my new menu'}
        response = self.client.post('/menu/', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        final_number_of_menus = Menu.objects.all().count()
        number_of_menus_created = final_number_of_menus - initial_number_of_menus
        self.assertEqual(number_of_menus_created, 0)
        self.client.logout()

    def test_update_success(self):
        """Test that checks success scenario for updating menu"""
        menu = Menu.objects.create(name='name to be changed', description='description to be changed')
        menu_pk = menu.pk
        self.client.login(username=self.TEST_SU_NAME, password=self.TEST_SU_PASSWORD)
        new_name = 'updated name'
        new_description = 'updated description'
        request_data = {'name': new_name, 'description': new_description}
        response = self.client.put(f'/menu/{menu_pk}', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_menu = Menu.objects.get(pk=menu_pk)
        self.assertEqual(updated_menu.name, new_name)
        self.assertEqual(updated_menu.description, new_description)
        self.client.logout()

    def test_update_failure(self):
        """Test that checks failure scenario for updating menu"""
        menu = Menu.objects.create(name='name to be changed', description='description to be changed')
        self.client.login(username=self.TEST_SU_NAME, password=self.TEST_SU_PASSWORD)
        request_data = {'description': 'updated description'}
        response = self.client.put(f'/menu/{menu.pk}', request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_delete_success(self):
        """Test that checks success scenario for deleting menu"""
        menu = Menu.objects.create(name='menu to be deleted name', description='menu to be deleted description')
        initial_number_of_menus = Menu.objects.all().count()
        self.client.login(username=self.TEST_SU_NAME, password=self.TEST_SU_PASSWORD)
        response = self.client.delete(f'/menu/{menu.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        final_number_of_menus = Menu.objects.all().count()
        number_of_menus_deleted = initial_number_of_menus - final_number_of_menus
        self.assertEqual(number_of_menus_deleted, 1)
        self.client.logout()

    def test_delete_failure(self):
        """Test that checks failure scenario for deleting menu with pk that does not exist"""
        Menu.objects.create(name='menu to be deleted name', description='menu to be deleted description')
        initial_number_of_menus = Menu.objects.all().count()
        self.client.login(username=self.TEST_SU_NAME, password=self.TEST_SU_PASSWORD)
        response = self.client.delete('/menu/10000000')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        final_number_of_menus = Menu.objects.all().count()
        number_of_menus_deleted = initial_number_of_menus - final_number_of_menus
        self.assertEqual(number_of_menus_deleted, 0)
        self.client.logout()

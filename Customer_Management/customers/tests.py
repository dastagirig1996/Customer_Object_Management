# customers/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import Customer
import jwt
from django.conf import settings
import datetime
import time

private_key = "gchvbnmpltfb3opmfnic4+54sff"
class CustomerAPITestCase(APITestCase):
   
    def setUp(self):
        # Create a test user/customer
        self.customer = Customer.objects.create(
            first_name="John", last_name="Doe",
            date_of_birth="1990-01-01", phone_number="1234567890",
            # ip = "187.87.85.125"
        )
        self.token = self.create_access_token(self.customer.id)
 
    def create_access_token(self, user_id):
        payload = {
            'user_id': user_id,
            # 'login_ip':ip,
            'exp': time.time() + 20,
        }
        access_token = jwt.encode(payload, private_key, algorithm='HS256')
        return access_token
 
    def test_customer_creation(self):
        url = reverse('list_create')
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1985-05-15",
            "phone_number": "8487654321"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   
    def test_customer_update(self):
        url = reverse('customer-detail', args=[self.customer.id])
        data = {"first_name": "UpdatedName"}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_customer_delete(self):
        url = reverse('customer-detail', args=[self.customer.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 
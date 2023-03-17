from core.models import Contact
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class ContactTestCase(APITestCase):
    name = "Billy Smith"
    client = APIClient()
    url = "/contact/"

    def setUp(self):
        self.data = {
            "name": self.name,
            "message": "test message",
            "email": "billysmith@test.com",
        }

    def test_create_contact(self):
        """Normal case creating a contact."""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().title, self.name)

    def test_create_contact_without_name(self):
        """Creating a contact but without name."""
        self.data.pop("name")
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_blank_name(self):
        """Creating a contact but the name is an empty string."""
        response = self.client.post(self.url, {**self.data, "name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_without_message(self):
        """Creating a contact but without message."""
        self.data.pop("message")
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_blank_message(self):
        """Creating a contact but the message is an empty string."""
        response = self.client.post(self.url, {**self.data, "message": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_without_email(self):
        """Creating a contact but without email."""
        self.data.pop("email")
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_blank_email(self):
        """Creating a contact but the email is an empty string."""
        response = self.client.post(self.url, {**self.data, "email": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_invalid_email(self):
        """Creating a contact but the email is invalid."""
        response = self.client.post(self.url, {**self.data, "email": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

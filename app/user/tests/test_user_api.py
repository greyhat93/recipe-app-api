"""Tests for the user api"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL =reverse("user:token")
ME_URL = reverse('user:me')


def create_user(**params):
    """Create return new user."""
    return get_user_model().objects.create_user(**params)

class PublicApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_sucess(self):
        """Test creating a user is successful."""
        payload ={
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test user"
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload.get("email"))
        self.assertTrue(user.check_password(payload.get("password")))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user email is existed."""

        payload ={
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test user"
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password is too short."""
        payload ={
            "email": "test@example.com",
            "password": "t123",
            "name": "test user"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload.get('email')
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test generates Token for valid credentails."""
        user_details ={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'test@123'
        }
        create_user(**user_details)
        payload ={
            'email': 'test@example.com',
            'password': 'test@123'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentails(self):
        """Test return error if credentails invalid."""

        create_user(email='test@example.com',password ='goodpass')
        payload = {
            'email':'test@example.com',
            'password': 'badpasss'
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test return error if password is blank"""

        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authetication."""
    def setUp(self):
        payload ={
            "email" : 'test@example.com',
            "password" :'test123',
            "name":'Test User'
        }
        self.user = create_user(
           **payload
        )
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)


    def test_retrive_profile_sucess(self):
        """Test retriving profile for logged in user."""


        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email

        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the autheticated user."""
        payload = {
            'name': 'updated name',
            'password': 'new password',

        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload.get('name'))
        self.assertTrue(self.user.check_password(payload.get('password')))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


"""Tests for the models
"""


from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models."""

    def test_create_user_with_email_success(self):
        """Test create a user with an email."""

        email = 'test@example.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normailze(self):
        """Test for normalized email for the new users."""
        email_testing = [
            ["TEST1@example.com", "TEST1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["test3@EXAMPLE.com", "test3@example.com"],
            ["test4@example.COM", "test4@example.com"]
        ]

        for email, expected_email in email_testing:
            user = get_user_model().objects.create_user(
                email= email,
                password = 'test123'
            )
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a value error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                'password123'
            )

    def test_create_super_user(self):
        """Test creating new super user."""

        super_user = get_user_model().objects.create_superuser(
            email = 'test123@example.com',
            password = 'test123'
        )
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
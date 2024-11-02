from django.test import TestCase, Client, TransactionTestCase
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class BaseAuthAPITest(TransactionTestCase):
    def setUp(self):
        """Run before each test method"""
        self.client = Client()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }

    def tearDown(self):
        """Run after each test method"""
        User.objects.filter(username=self.user_data['username']).delete()

class RegisterAPITest(BaseAuthAPITest):
    def setUp(self):
        super().setUp()
        self.register_url = '/api/auth/register'

    def test_successful_registration(self):
        """Test successful user registration"""
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue('tokens' in response.json())
        self.assertTrue('access' in response.json()['tokens'])
        self.assertTrue('refresh' in response.json()['tokens'])
        self.assertEqual(response.json()['message'], 'User created successfully')
        
        # Verify user was created in database
        self.assertTrue(
            User.objects.filter(username=self.user_data['username']).exists()
        )

    def test_duplicate_username_registration(self):
        """Test registration with existing username fails"""
        # First create a user
        User.objects.create_user(
            username=self.user_data['username'],
            email='existing@test.com',
            password=self.user_data['password']
        )

        # Try to register with same username
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_email_registration(self):
        """Test registration with invalid email fails"""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['email'] = 'invalid-email'
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 422)
        self.assertTrue('detail' in response.json())

    def test_missing_fields_registration(self):
        """Test registration with missing required fields fails"""
        invalid_data = {
            "username": "testuser"
            # missing email and password
        }
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 422)  # Validation error

class LoginAPITest(BaseAuthAPITest):
    def setUp(self):
        super().setUp()
        self.login_url = '/api/auth/login'
        # Create a test user for login tests
        self.user = User.objects.create_user(**self.user_data)

    def test_successful_login(self):
        """Test successful user login"""
        response = self.client.post(
            self.login_url,
            data=json.dumps({
                "username": self.user_data['username'],
                "password": self.user_data['password']
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tokens' in response.json())
        self.assertTrue('access' in response.json()['tokens'])
        self.assertTrue('refresh' in response.json()['tokens'])

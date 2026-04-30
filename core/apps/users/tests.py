from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserUpdateSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    """Tests for UserSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            phone="+1234567890",
            password="testpass123",
            role=User.Role.CLIENT,
            address="Test Address"
        )
    
    def test_user_serializer_read_only_fields(self):
        """Test that serializer fields are read-only"""
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        self.assertEqual(data['username'], "testuser")
        self.assertEqual(data['phone'], "+1234567890")
        self.assertEqual(data['role'], User.Role.CLIENT)
        self.assertIn('id', data)
        self.assertIn('date_joined', data)


class RegisterSerializerTest(TestCase):
    """Tests for RegisterSerializer"""
    
    def test_create_user_with_valid_data(self):
        """Test creating user with valid data"""
        data = {
            "username": "newuser",
            "phone": "+1234567891",
            "password": "securepass123",
            "role": User.Role.CLIENT,
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.phone, "+1234567891")
        self.assertTrue(user.check_password("securepass123"))
        self.assertEqual(user.role, User.Role.CLIENT)
    
    def test_password_minimum_length(self):
        """Test password minimum length validation"""
        data = {
            "username": "shortpassuser",
            "phone": "+1234567892",
            "password": "12345",  # Only 5 chars
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
    
    def test_cannot_register_as_admin(self):
        """Test that users cannot register as admin"""
        data = {
            "username": "adminuser",
            "phone": "+1234567893",
            "password": "securepass123",
            "role": User.Role.ADMIN,
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('role', serializer.errors)
    
    def test_default_role_is_client(self):
        """Test that default role is CLIENT when not specified"""
        data = {
            "username": "defaultroleuser",
            "phone": "+1234567894",
            "password": "securepass123",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.role, User.Role.CLIENT)
    
    def test_phone_uniqueness(self):
        """Test that phone number must be unique"""
        User.objects.create_user(
            username="existinguser",
            phone="+1234567895",
            password="testpass123"
        )
        data = {
            "username": "duplicateuser",
            "phone": "+1234567895",  # Same phone
            "password": "securepass123",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone', serializer.errors)


class LoginSerializerTest(TestCase):
    """Tests for LoginSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="loginuser",
            phone="+1234567896",
            password="correctpass123"
        )
    
    def test_login_with_correct_credentials(self):
        """Test login with correct credentials"""
        data = {
            "username": "loginuser",
            "password": "correctpass123",
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
    
    def test_login_with_wrong_password(self):
        """Test login with wrong password"""
        data = {
            "username": "loginuser",
            "password": "wrongpassword",
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
    
    def test_login_with_nonexistent_user(self):
        """Test login with nonexistent username"""
        data = {
            "username": "nonexistentuser",
            "password": "somepassword",
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_login_with_inactive_user(self):
        """Test login with inactive/disabled user"""
        self.user.is_active = False
        self.user.save()
        data = {
            "username": "loginuser",
            "password": "correctpass123",
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class UserUpdateSerializerTest(TestCase):
    """Tests for UserUpdateSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="updateuser",
            phone="+1234567897",
            password="testpass123",
            address="Old Address"
        )
    
    def test_update_username(self):
        """Test updating username only"""
        serializer = UserUpdateSerializer(self.user, data={"username": "newusername"}, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "newusername")
    
    def test_update_phone(self):
        """Test updating phone only"""
        serializer = UserUpdateSerializer(self.user, data={"phone": "+9876543210"}, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.phone, "+9876543210")
    
    def test_update_address(self):
        """Test updating address only"""
        serializer = UserUpdateSerializer(self.user, data={"address": "New Address"}, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.address, "New Address")
    
    def test_cannot_update_role(self):
        """Test that role cannot be updated via this serializer"""
        serializer = UserUpdateSerializer(self.user, data={"role": User.Role.WORKER}, partial=True)
        # Role is not in fields, so it should be ignored
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.role, User.Role.CLIENT)  # Unchanged


class RegisterViewTest(APITestCase):
    """Tests for RegisterView API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_register_success(self):
        """Test successful registration returns tokens"""
        data = {
            "username": "apitestuser",
            "phone": "+1111111111",
            "password": "testpass123",
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_register_invalid_data(self):
        """Test registration with invalid data"""
        data = {
            "username": "",  # Empty username
            "phone": "+1111111111",
            "password": "testpass123",
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    """Tests for LoginView API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="loginapitest",
            phone="+2222222222",
            password="loginpass123"
        )
    
    def test_login_success(self):
        """Test successful login returns tokens"""
        data = {
            "username": "loginapitest",
            "password": "loginpass123",
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
    
    def test_login_failure(self):
        """Test login with wrong credentials"""
        data = {
            "username": "loginapitest",
            "password": "wrongpassword",
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MyProfileViewTest(APITestCase):
    """Tests for MyProfileView API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="profileuser",
            phone="+3333333333",
            password="profilepass123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
    
    def test_get_profile_authenticated(self):
        """Test getting own profile when authenticated"""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "profileuser")
    
    def test_patch_profile_update(self):
        """Test updating own profile"""
        data = {"address": "Updated Address"}
        response = self.client.patch('/api/users/me/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], "Updated Address")
    
    def test_profile_requires_authentication(self):
        """Test that profile endpoint requires authentication"""
        self.client.credentials()  # Clear credentials
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTest(TestCase):
    """Tests for User model"""
    
    def test_user_creation(self):
        """Test creating user with all fields"""
        user = User.objects.create_user(
            username="modeltestuser",
            phone="+4444444444",
            password="modelpass123",
            role=User.Role.WORKER,
            address="Model Test Address"
        )
        self.assertEqual(str(user), "modeltestuser (worker)")
        self.assertEqual(user.role, User.Role.WORKER)
    
    def test_user_role_choices(self):
        """Test user role choices"""
        self.assertIn(User.Role.CLIENT, [choice[0] for choice in User.Role.choices])
        self.assertIn(User.Role.WORKER, [choice[0] for choice in User.Role.choices])
        self.assertIn(User.Role.ADMIN, [choice[0] for choice in User.Role.choices])
    
    def test_user_default_role(self):
        """Test that default role is CLIENT"""
        user = User.objects.create_user(
            username="defaultrole",
            phone="+5555555555",
            password="testpass123"
        )
        self.assertEqual(user.role, User.Role.CLIENT)

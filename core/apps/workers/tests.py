from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

from core.apps.users.models import User
from .models import ServiceCategory, WorkerProfile
from .serializers import ServiceCategorySerializer, WorkerProfileSerializer, WorkerProfileWriteSerializer


User = get_user_model()


class ServiceCategoryModelTest(TestCase):
    """Tests for ServiceCategory model"""
    
    def test_category_creation(self):
        """Test creating a service category"""
        category = ServiceCategory.objects.create(name="Plumbing")
        self.assertEqual(str(category), "Plumbing")
        self.assertEqual(category.name, "Plumbing")
    
    def test_category_unique_name(self):
        """Test that category names must be unique"""
        ServiceCategory.objects.create(name="Electrical")
        with self.assertRaises(Exception):
            ServiceCategory.objects.create(name="Electrical")


class WorkerProfileModelTest(TestCase):
    """Tests for WorkerProfile model"""
    
    def setUp(self):
        self.worker = User.objects.create_user(
            username="workeruser",
            phone="+1234567890",
            password="testpass123",
            role=User.Role.WORKER
        )
        self.profile = WorkerProfile.objects.create(
            user=self.worker,
            profession="Plumber",
            experience_years=5,
            average_rating=4.5,
            completed_jobs=10,
            is_available=True
        )
    
    def test_profile_creation(self):
        """Test creating a worker profile"""
        self.assertEqual(str(self.profile), "workeruser — Plumber")
        self.assertEqual(self.profile.profession, "Plumber")
        self.assertEqual(self.profile.experience_years, 5)
    
    def test_calculate_score(self):
        """Test worker score calculation formula"""
        # Score = (average_rating × 0.6) + (completed_jobs × 0.4)
        expected_score = (4.5 * 0.6) + (10 * 0.4)
        self.assertEqual(self.profile.calculate_score(), expected_score)
    
    def test_default_values(self):
        """Test default field values"""
        worker2 = User.objects.create_user(
            username="newworker",
            phone="+0987654321",
            password="testpass123",
            role=User.Role.WORKER
        )
        profile2 = WorkerProfile.objects.create(
            user=worker2,
            profession="Electrician"
        )
        self.assertEqual(profile2.experience_years, 0)
        self.assertEqual(profile2.average_rating, 0.0)
        self.assertEqual(profile2.completed_jobs, 0)
        self.assertTrue(profile2.is_available)
    
    def test_one_to_one_with_user(self):
        """Test that each user can only have one worker profile"""
        with self.assertRaises(Exception):
            WorkerProfile.objects.create(
                user=self.worker,
                profession="Another Profession"
            )


class ServiceCategorySerializerTest(TestCase):
    """Tests for ServiceCategorySerializer"""
    
    def test_serialize_category(self):
        """Test serializing a service category"""
        category = ServiceCategory.objects.create(name="Carpentry")
        serializer = ServiceCategorySerializer(category)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Carpentry")


class WorkerProfileSerializerTest(TestCase):
    """Tests for WorkerProfileSerializer"""
    
    def setUp(self):
        self.worker = User.objects.create_user(
            username="serializerworker",
            phone="+1111111111",
            password="testpass123",
            role=User.Role.WORKER
        )
        self.profile = WorkerProfile.objects.create(
            user=self.worker,
            profession="Painter",
            experience_years=3,
            average_rating=4.0,
            completed_jobs=5,
            is_available=True
        )
    
    def test_serialize_worker_profile(self):
        """Test serializing a worker profile with nested user data"""
        serializer = WorkerProfileSerializer(self.profile)
        data = serializer.data
        
        self.assertIn('user', data)
        self.assertIn('profession', data)
        self.assertIn('score', data)
        self.assertEqual(data['profession'], "Painter")
        self.assertEqual(data['experience_years'], 3)
    
    def test_score_calculation_in_serializer(self):
        """Test that score is calculated correctly in serializer"""
        serializer = WorkerProfileSerializer(self.profile)
        data = serializer.data
        expected_score = round((4.0 * 0.6) + (5 * 0.4), 2)
        self.assertEqual(data['score'], expected_score)
    
    def test_read_only_fields(self):
        """Test that certain fields are read-only"""
        # average_rating, completed_jobs, created_at should be read-only
        self.assertIn('average_rating', WorkerProfileSerializer.Meta.read_only_fields)
        self.assertIn('completed_jobs', WorkerProfileSerializer.Meta.read_only_fields)


class WorkerProfileWriteSerializerTest(TestCase):
    """Tests for WorkerProfileWriteSerializer"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.worker = User.objects.create_user(
            username="writeworker",
            phone="+2222222222",
            password="testpass123",
            role=User.Role.WORKER
        )
        self.refresh = RefreshToken.for_user(self.worker)
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
    
    def test_create_profile(self):
        """Test creating a worker profile"""
        data = {
            "profession": "Welder",
            "experience_years": 7,
            "is_available": True
        }
        serializer = WorkerProfileWriteSerializer(
            data=data,
            context={"request": type('obj', (object,), {'user': self.worker})()}
        )
        self.assertTrue(serializer.is_valid())
        profile = serializer.save()
        self.assertEqual(profile.user, self.worker)
        self.assertEqual(profile.profession, "Welder")
    
    def test_cannot_create_duplicate_profile(self):
        """Test that a worker cannot have multiple profiles"""
        WorkerProfile.objects.create(
            user=self.worker,
            profession="First Profession"
        )
        data = {"profession": "Second Profession"}
        serializer = WorkerProfileWriteSerializer(
            data=data,
            context={"request": type('obj', (object,), {'user': self.worker})()}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class WorkerListViewTest(APITestCase):
    """Tests for WorkerListView API endpoint"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.category = ServiceCategory.objects.create(name="Plumbing")
        
        # Create some workers
        for i in range(15):
            worker = User.objects.create_user(
                username=f"worker{i}",
                phone=f"+{i:010d}",
                password="testpass123",
                role=User.Role.WORKER
            )
            WorkerProfile.objects.create(
                user=worker,
                profession="Plumbing" if i % 2 == 0 else "Electrical",
                experience_years=i,
                average_rating=4.0 + (i * 0.1),
                completed_jobs=i * 2,
                is_available=(i % 3 != 0)  # Some unavailable
            )
    
    def test_list_workers_pagination(self):
        """Test that workers list is paginated"""
        response = self.client_api.get('/api/workers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
    
    def test_filter_by_category(self):
        """Test filtering workers by category"""
        response = self.client_api.get(f'/api/workers/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return Plumbing workers
        for result in response.data['results']:
            self.assertEqual(result['profession'], "Plumbing")
    
    def test_search_by_profession(self):
        """Test searching workers by profession keyword"""
        response = self.client_api.get('/api/workers/?search=Plumb')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data['results']:
            self.assertIn("Plumb", result['profession'])
    
    def test_workers_sorted_by_score(self):
        """Test that workers are sorted by score descending"""
        response = self.client_api.get('/api/workers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        scores = [worker['score'] for worker in results]
        self.assertEqual(scores, sorted(scores, reverse=True))


class WorkerDetailViewTest(APITestCase):
    """Tests for WorkerDetailView API endpoint"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.worker = User.objects.create_user(
            username="detailworker",
            phone="+3333333333",
            password="testpass123",
            role=User.Role.WORKER
        )
        self.profile = WorkerProfile.objects.create(
            user=self.worker,
            profession="Mechanic",
            experience_years=10
        )
    
    def test_get_worker_detail(self):
        """Test getting a specific worker's details"""
        response = self.client_api.get(f'/api/workers/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profession'], "Mechanic")
    
    def test_worker_not_found(self):
        """Test 404 for non-existent worker"""
        response = self.client_api.get('/api/workers/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MyWorkerProfileViewTest(APITestCase):
    """Tests for MyWorkerProfileView API endpoint"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.worker = User.objects.create_user(
            username="myprofileworker",
            phone="+4444444444",
            password="testpass123",
            role=User.Role.WORKER
        )
        self.refresh = RefreshToken.for_user(self.worker)
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
    
    def test_get_own_profile(self):
        """Test worker can get their own profile"""
        profile = WorkerProfile.objects.create(
            user=self.worker,
            profession="Developer"
        )
        response = self.client_api.get('/api/workers/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profession'], "Developer")
    
    def test_update_own_profile(self):
        """Test worker can update their own profile"""
        WorkerProfile.objects.create(
            user=self.worker,
            profession="Developer",
            experience_years=5
        )
        data = {"profession": "Senior Developer", "experience_years": 10}
        response = self.client_api.patch('/api/workers/me/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profession'], "Senior Developer")
        self.assertEqual(response.data['experience_years'], 10)
    
    def test_non_worker_cannot_access(self):
        """Test that non-workers cannot access worker profile endpoints"""
        client_user = User.objects.create_user(
            username="clientuser",
            phone="+5555555555",
            password="testpass123",
            role=User.Role.CLIENT
        )
        refresh = RefreshToken.for_user(client_user)
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = self.client_api.get('/api/workers/me/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_no_profile_yet(self):
        """Test error when worker doesn't have a profile yet"""
        response = self.client_api.get('/api/workers/me/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryListViewTest(APITestCase):
    """Tests for CategoryListView API endpoint"""
    
    def setUp(self):
        self.client_api = APIClient()
        ServiceCategory.objects.create(name="Plumbing")
        ServiceCategory.objects.create(name="Electrical")
        ServiceCategory.objects.create(name="Carpentry")
    
    def test_list_categories(self):
        """Test listing all categories"""
        response = self.client_api.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class CategoryCreateViewTest(APITestCase):
    """Tests for CategoryCreateView API endpoint"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.admin = User.objects.create_user(
            username="adminuser",
            phone="+6666666666",
            password="adminpass123",
            role=User.Role.ADMIN
        )
        self.refresh = RefreshToken.for_user(self.admin)
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
    
    def test_admin_can_create_category(self):
        """Test that admin can create categories"""
        data = {"name": "New Category"}
        response = self.client_api.post('/api/categories/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Category")
    
    def test_non_admin_cannot_create_category(self):
        """Test that non-admins cannot create categories"""
        client_user = User.objects.create_user(
            username="clientuser2",
            phone="+7777777777",
            password="testpass123",
            role=User.Role.CLIENT
        )
        refresh = RefreshToken.for_user(client_user)
        self.client_api.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {"name": "Unauthorized Category"}
        response = self.client_api.post('/api/categories/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

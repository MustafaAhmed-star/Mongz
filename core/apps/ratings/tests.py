from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.orders.models import Order
from apps.workers.models import ServiceCategory, WorkerProfile
from apps.ratings.models import Rating


User = get_user_model()


class WorkerRatingsViewTest(APITestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.category = ServiceCategory.objects.create(name="Electrical")
        self.client_user = User.objects.create_user(
            username="ratingclient",
            phone="+201111111111",
            password="testpass123",
            role=User.Role.CLIENT,
        )
        self.worker_user = User.objects.create_user(
            username="ratingworker",
            phone="+201111111112",
            password="testpass123",
            role=User.Role.WORKER,
        )
        self.worker_profile = WorkerProfile.objects.create(
            user=self.worker_user,
            category=self.category,
        )
        self.order = Order.objects.create(
            client=self.client_user,
            worker=self.worker_user,
            service_category=self.category,
            description="Install a new socket.",
            phone=self.client_user.phone,
            status=Order.COMPLETED,
        )
        Rating.objects.create(
            order=self.order,
            client=self.client_user,
            worker=self.worker_user,
            stars=5,
            review="Excellent service.",
        )
        refresh = RefreshToken.for_user(self.client_user)
        self.client_api.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_worker_ratings_are_paginated(self):
        response = self.client_api.get(f"/api/workers/{self.worker_profile.id}/ratings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"][0]["comment"], "Excellent service.")
        self.assertEqual(response.data["results"][0]["stars"], 5)
        self.assertEqual(response.data["results"][0]["client_name"], "ratingclient")

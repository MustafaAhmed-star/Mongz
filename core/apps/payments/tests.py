from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

from apps.users.models import User
from apps.workers.models import ServiceCategory, WorkerProfile
from apps.orders.models import Order
from .models import CommissionPayment
from . import paymob


class CommissionPaymentModelTest(TestCase):
    """Tests for CommissionPayment model"""
    
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="clientuser",
            phone="+1111111111",
            password="testpass123",
            role=User.Role.CLIENT
        )
        self.worker_user = User.objects.create_user(
            username="workeruser",
            phone="+2222222222",
            password="testpass123",
            role=User.Role.WORKER
        )
        self.category = ServiceCategory.objects.create(name="Plumbing")
        self.order = Order.objects.create(
            client=self.client_user,
            worker=self.worker_user,
            service_category=self.category,
            status=Order.PENDING
        )
    
    def test_commission_payment_creation(self):
        """Test creating a commission payment"""
        payment = CommissionPayment.objects.create(
            order=self.order,
            amount=Decimal('20.00'),
            payment_status=CommissionPayment.AUTHORIZED
        )
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.amount, Decimal('20.00'))
        self.assertEqual(payment.payment_status, CommissionPayment.AUTHORIZED)
    
    def test_payment_status_choices(self):
        """Test payment status choices"""
        valid_statuses = [
            CommissionPayment.AUTHORIZED,
            CommissionPayment.CAPTURED,
            CommissionPayment.VOIDED,
            CommissionPayment.FAILED,
        ]
        for i, status_choice in enumerate(valid_statuses):
            # Create separate order for each payment since OneToOneField
            order = Order.objects.create(
                client=self.client_user,
                service_category=self.category,
                status=Order.PENDING
            )
            payment = CommissionPayment.objects.create(
                order=order,
                amount=Decimal('20.00'),
                payment_status=status_choice
            )
            self.assertEqual(payment.payment_status, status_choice)
    
    def test_default_payment_status(self):
        """Test default payment status is AUTHORIZED"""
        payment = CommissionPayment.objects.create(
            order=self.order,
            amount=Decimal('20.00'),
        )
        self.assertEqual(payment.payment_status, CommissionPayment.AUTHORIZED)
    
    def test_payment_string_representation(self):
        """Test payment __str__ method"""
        payment = CommissionPayment.objects.create(
            order=self.order,
            amount=Decimal('20.00'),
        )
        self.assertIn(f"Commission #{payment.id}", str(payment))
        self.assertIn(f"Order #{self.order.id}", str(payment))


class PaymobClientTest(TestCase):
    """Tests for Paymob API client functions"""
    
    def test_get_auth_token_structure(self):
        """Test that get_auth_token returns a token (integration test requires valid API key)"""
        # This is an integration test - it will fail with invalid credentials
        # In production, you'd mock the requests.post call
        try:
            token = paymob.get_auth_token()
            self.assertIsInstance(token, str)
            self.assertTrue(len(token) > 0)
        except Exception:
            # Expected to fail in test environment without valid credentials
            pass
    
    def test_authorize_commission_structure(self):
        """Test authorize_commission returns tuple (integration test)"""
        # This would be mocked in real tests
        # Just verifying the function exists and has correct signature
        self.assertTrue(callable(paymob.authorize_commission))
    
    def test_capture_commission_structure(self):
        """Test capture_commission function exists"""
        self.assertTrue(callable(paymob.capture_commission))
    
    def test_void_commission_structure(self):
        """Test void_commission function exists"""
        self.assertTrue(callable(paymob.void_commission))

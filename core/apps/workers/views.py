from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import User
from .models import ServiceCategory, WorkerProfile
from .serializers import (
    ServiceCategorySerializer,
    WorkerProfileSerializer,
    WorkerProfileWriteSerializer,
)


# Service Categoies

class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = ServiceCategory.objects.all()
        return Response(ServiceCategorySerializer(categories, many=True).data)


class CategoryCreateView(APIView):
    #for admin only
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != User.Role.ADMIN:
            return Response(
                {"error": "Only admins can create categories."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ServiceCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Worker Profiles
class WorkerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        workers = WorkerProfile.objects.select_related("user").filter(
            user__is_active=True
        )
        return Response(WorkerProfileSerializer(workers, many=True).data)


class WorkerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers can create a worker profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = WorkerProfileWriteSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            profile = serializer.save()
            return Response(
                WorkerProfileSerializer(profile).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            worker = WorkerProfile.objects.select_related("user").get(pk=pk)
        except WorkerProfile.DoesNotExist:
            return Response(
                {"error": "Worker not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(WorkerProfileSerializer(worker).data)


class MyWorkerProfileView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers have a worker profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not hasattr(request.user, "worker_profile"):
            return Response(
                {"error": "You do not have a worker profile yet."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(WorkerProfileSerializer(request.user.worker_profile).data)

    def patch(self, request):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers can update a worker profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not hasattr(request.user, "worker_profile"):
            return Response(
                {"error": "You do not have a worker profile yet."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = WorkerProfileWriteSerializer(
            request.user.worker_profile,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(WorkerProfileSerializer(request.user.worker_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

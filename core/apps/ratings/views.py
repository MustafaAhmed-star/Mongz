from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from .models import Rating
from .serializers import RatingSerializer


class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != User.Role.CLIENT:
            return Response(
                {"error": "Only clients can submit ratings."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = RatingSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            rating = serializer.save()
            return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerRatingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        ratings = Rating.objects.filter(worker=request.user).order_by('-created_at')

        if not ratings.exists():
            return Response(
                {"message": "No ratings found for this worker."},
                status=status.HTTP_200_OK)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
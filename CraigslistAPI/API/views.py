from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from .models import Listing
from .serializers import ListingSerializer, ListingCreateUpdateSerializer

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from .models import Listing


class ListingCreateAPIView(CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingCreateUpdateSerializer


class ListingDetailAPIView(RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingUpdateAPIView(UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingCreateUpdateSerializer


class ListingDeleteAPIView(DestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingListAPIView(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

# # Create your views here.
# class ListingAll(APIView):
#     pagination_class = LimitOffsetPagination
#     def get(self, request):
#         queryset = Listing.objects.all()
#         serializer = ListingSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# class ListingPost(APIView):
#     def post(self):
#         pass
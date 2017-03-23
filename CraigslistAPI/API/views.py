from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from .models import Listing
from .serializers import ListingSerializer

from rest_framework.generics import ListAPIView
from .models import Listing

class ListingAPIView(ListAPIView):
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
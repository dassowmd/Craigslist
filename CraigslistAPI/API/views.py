from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from .models import Listing
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .serializers import ListingSerializer, ListingCreateUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .models import Listing


class ListingCreateAPIView(CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListingDetailAPIView(RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingCreateUpdateSerializer


class ListingDeleteAPIView(DestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingListAPIView(ListAPIView):
    serializer_class = ListingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user', 'CL_Item_ID', 'KeyParam', 'RSS_Feed_String']
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Listing.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(user_id_icontains=query)|
                Q(Cl_Item_ID_icontains=query)|
                Q(KeyParam_icontains=query)|
                # Q(ValueParam_icontains=query)|
                Q(RSS_Feed_String_icontains=query)
            ).distinct()
        return queryset_list

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
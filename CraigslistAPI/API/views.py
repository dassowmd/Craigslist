from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .serializers import ListingSerializer, ListingCreateUpdateSerializer, IDListingSerializer, ListingRehydratedSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .models import Listing, ListingRehydrated
import json


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
    pagination_class.default_limit = 100
    pagination_class.max_limit = 1000

    def get_queryset(self, *args, **kwargs):
        queryset_list = Listing.objects.all()
        query = self.request.GET.get('q')
        # print(query)
        if query:
            queryset_list = queryset_list.filter(
                # Q(user__icontains=query)
                Q(Cl_Item_ID__icontains=query) |
                Q(KeyParam__icontains=query) |
                Q(ValueParam__icontains=query) |
                Q(RSS_Feed_String__icontains=query)
            ).distinct()
        return queryset_list

class ListingclIDListAPIView(ListAPIView):
    serializer_class = IDListingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user', 'CL_Item_ID', 'KeyParam', 'RSS_Feed_String']
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 100
    pagination_class.max_limit = 1000

    def get_queryset(self, *args, **kwargs):
        queryset_list = Listing.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(user_id_icontains=query) |
                Q(Cl_Item_ID_icontains=query) |
                Q(KeyParam_icontains=query) |
                # Q(ValueParam_icontains=query)|
                Q(RSS_Feed_String_icontains=query)
            ).distinct()
        return queryset_list


class ListingRehydratedAPIView(RetrieveAPIView):
    serializer_class = ListingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['Cl_Item_ID']
    lookup_field = ['Cl_Item_ID']

    def get_queryset(self, *args, **kwargs):
        # rehydratedResult = ListingRehydrated
        queryset_list = Listing.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(Cl_Item_ID__exact=query)
            ).distinct()
            # parameters ={}
            # for i in queryset_list:
            #     if rehydratedResult.Cl_Item_ID == None:
            #         rehydratedResult.user = i.user
            #         rehydratedResult.Cl_Item_ID = i.Cl_Item_ID
            #         rehydratedResult.ScrapedDateTime = i.ScrapedDateTime
            #         rehydratedResult.RSS_Feed_String = i.RSS_Feed_String
            #
            #     d = {}
            #     d[i.KeyParam] = i.ValueParam
            #     parameters.update(d)
            # rehydratedResult.jsonParameters = json.dumps(parameters)
        return queryset_list

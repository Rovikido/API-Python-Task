from datetime import date

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, F

from menu.models import Restaurant, Menu, Vote
from menu.serializers import RestaurantSerializer, MenuSerializer, UserSerializer, VoteSerializer


@api_view(['GET'])
def get_restaurant_list(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_restaurant(request):
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()


@api_view(['GET'])
def get_all_menus(request):
    menus = Menu.objects.all()
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_menus_for_date(request):
    day = request.query_params.get('day', date.today())
    menus = Menu.objects.filter(menu_date=day)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_result_for_date(request):
    day = request.query_params.get('day', date.today())
    most_voted_menu = (
        Menu.objects
        .filter(menu_date=day)
        .annotate(vote_count=Count('vote'))
        .order_by(F('vote_count').desc(nulls_last=True))
        .first()
    )
    if most_voted_menu:
        serializer = MenuSerializer(most_voted_menu)
        return Response(serializer.data)
    else:
        return Response({'message': 'No menus found for the specified day.'}, status=404)

@api_view(['POST'])
def add_menu(request):
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()


@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vote(request):
    user = request.user
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user'] = user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
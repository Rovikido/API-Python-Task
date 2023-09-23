from datetime import date

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, F
from django.contrib.auth.models import User

from menu.models import Restaurant, Menu, Vote
from menu.serializers import RestaurantSerializer, MenuSerializer, UserSerializer, EmployeeProfileSerializer, VoteSerializer
from .models import EmployeeProfile
from .permissions import CanVotePermission, APIVersionPermission


@api_view(['GET'])
def get_restaurant_list(request):
    """
    Get a list of all restaurants.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing a list of restaurants.
    """
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, APIVersionPermission])
def add_restaurant(request):
    """
    Add a new restaurant.

    Args:
        request: HTTP request object.

    Returns:
        Response: Empty response.
    """
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()


@api_view(['GET'])
def get_all_menus(request):
    """
    Get a list of all menus.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing a list of menus.
    """
    menus = Menu.objects.all()
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_menus_for_date(request):
    """
    Get a list of menus for a specific date.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing a list of menus for the specified date.
    """
    day = request.query_params.get('day', date.today())
    menus = Menu.objects.filter(menu_date=day)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_result_for_date(request):
    """
    Get the most voted menu for a specific date.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing the most voted menu for the specified date.
    """
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
        return Response({'message': f'No menus found for the specified day({day}).'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated, APIVersionPermission])
def add_menu(request):
    """
    Add a new menu.

    Args:
        request: HTTP request object.

    Returns:
        Response: Empty response.
    """
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated, CanVotePermission, APIVersionPermission])
def vote(request):
    """
    Send a vote for a menu.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response with the vote data.
    """
    user = request.user
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user'] = user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([APIVersionPermission])
def register_user(request):
    """
    Register a new user.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response with user data.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user_type = request.data.get('user_type')

    if user_type == 'basic':
        user = User.objects.create(username=username, password=password)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif user_type == 'employee':
        user = User.objects.create(username=username, password=password)
        profile = EmployeeProfile.objects.create(user=user)
        EmployeeProfileSerializer(profile)
        return Response(UserSerializer(user).data)
    else:
        return Response({'error': 'Invalid user type'}, status=400)


class CombinedTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view for obtaining access tokens.

    This view combines user and employee profiles for authentication.

    Args:
        TokenObtainPairView: The base token obtain view.

    Methods:
        post: Handle the token request and combine user and employee profiles for authentication.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user is None:
            user = EmployeeProfile.objects.filter(username=username).first().user
        
        if user and user.password == password:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response({'detail': 'No active account found with the given credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

import pytest
import json
from datetime import datetime

from django.contrib.auth.models import User
from menu.models import Restaurant, Menu, Vote
from menu.serializers import RestaurantSerializer, MenuSerializer, UserSerializer, VoteSerializer


@pytest.fixture
def restaurant_data():
    return {'id': 1, 'name': 'Test Restaurant'}


@pytest.fixture
def menu_json_data():
    return {'test_product_1':10, 'test_product_2':20}


@pytest.mark.django_db
def test_serialize_restaurant(restaurant_data):
    serializer = RestaurantSerializer(data=restaurant_data)
    assert serializer.is_valid()
    instance = serializer.save()
    serialized_data = serializer.data
    serialized_data['id'] = instance.id
    assert serialized_data == restaurant_data

@pytest.mark.django_db
def test_serialize_menu(menu_json_data):
    restaurant = Restaurant.objects.create(name='Test Restaurant')
    menu_data = {'id': 1, 'name': 'Test Menu', 'restaurant': restaurant.pk, 
                 'menu_data': menu_json_data, 'menu_date':datetime.now().strftime('%Y-%m-%d')}
    serializer = MenuSerializer(data=menu_data)
    if not serializer.is_valid():
        print(serializer.errors)
    assert serializer.is_valid()
    instance = serializer.save()
    serialized_data = serializer.data
    serialized_data['id'] = instance.id
    assert serialized_data == menu_data

@pytest.mark.django_db
def test_serialize_user():
    user_data = {'id': 1, 'username': 'testuser', 'email': 'test@example.com', 'password': 'qwerty12'}
    serializer = UserSerializer(data=user_data)
    if not serializer.is_valid():
        print(serializer.errors)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_serialize_vote(menu_json_data):
    restaurant = Restaurant.objects.create(name='Test Restaurant')
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    menu = Menu.objects.create(name='Test Menu', restaurant=restaurant, menu_data=menu_json_data)
    vote_data = {'id': 1, 'user': user.pk, 'menu': menu.pk, 'vote_date': datetime.now().strftime('%Y-%m-%d')}
    serializer = VoteSerializer(data=vote_data)
    assert serializer.is_valid()
    instance = serializer.save()
    serialized_data = serializer.data
    serialized_data['id'] = instance.id
    assert serialized_data == vote_data

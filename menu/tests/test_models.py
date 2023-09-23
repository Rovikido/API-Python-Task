from django.test import TestCase
from django.contrib.auth.models import User
from menu.models import Restaurant, Menu, Vote

import pytest
import json


@pytest.fixture
def menu_data():
    return json.dumps({'test_product_1':10, 'test_product_2':20})


@pytest.mark.django_db
def test_create_restaurant():
    restaurant = Restaurant.objects.create(name="Test Restaurant")
    assert restaurant.name == "Test Restaurant"

@pytest.mark.django_db
def test_create_menu(menu_data):
    restaurant = Restaurant.objects.create(name="Test Restaurant")
    menu = Menu.objects.create(name="Test Menu", restaurant=restaurant, menu_data=menu_data)
    assert menu.name == "Test Menu"
    assert menu.restaurant == restaurant

@pytest.mark.django_db
def test_create_vote(menu_data):
    user = User.objects.create_user(username="testuser", password="password123")
    restaurant = Restaurant.objects.create(name="Test Restaurant")
    menu = Menu.objects.create(name="Test Menu", restaurant=restaurant, menu_data=menu_data)
    vote = Vote.objects.create(user=user, menu=menu, vote_date="2023-09-23")
    
    assert vote.user == user
    assert vote.menu == menu
    assert str(vote.vote_date) == "2023-09-23"

@pytest.mark.django_db
def test_vote_unique_together_constraint(menu_data):
    user = User.objects.create_user(username="testuser", password="password123")
    restaurant = Restaurant.objects.create(name="Test Restaurant")
    menu = Menu.objects.create(name="Test Menu", restaurant=restaurant, menu_data=menu_data)
    
    Vote.objects.create(user=user, menu=menu, vote_date="2023-09-23")
    
    with pytest.raises(Exception):
        Vote.objects.create(user=user, menu=menu, vote_date="2023-09-23")

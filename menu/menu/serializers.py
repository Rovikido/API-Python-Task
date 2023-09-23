from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date

from .models import Restaurant, Menu, Vote, EmployeeProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Attributes:
        Meta (class): Configuration class for the serializer.
    """
    class Meta:
        model = User
        fields = '__all__'


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmployeeProfile model.

    Attributes:
        Meta (class): Configuration class for the serializer.
    """
    class Meta:
        model = EmployeeProfile
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model.

    Serializes restaurant data, including name, location, and other fields.

    Attributes:
        Meta (class): Configuration class for the serializer.
    """
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model.

    Serializes menu data, including the menu date and its related restaurant.

    Attributes:
        Meta (class): Configuration class for the serializer.

    Methods:
        validate_menu_date(value): Validates that the menu date is not in the past.
    """
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = '__all__'

    def validate_menu_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Menu date cannot be in the past.")
        return value


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.

    Serializes vote data, including the user who voted and the menu they voted for.

    Attributes:
        Meta (class): Configuration class for the serializer.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())

    class Meta:
        model = Vote
        fields = '__all__'

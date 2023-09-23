from django.contrib.auth.models import User
from django.db import models

from datetime import datetime


class EmployeeProfile(models.Model):
    """
    EmployeeProfile model is an alternative for User.

    This model is used to indicate wether the user can vote.

    Fields:
        user (User): One-to-one relationship with the User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Restaurant(models.Model):
    """
    Menu supliers.

    Fields:
        name (str): The name of the restaurant.

    Methods:
        __str__(): String representation of the restaurant.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    Menu for a specific date and restaurant.

    Fields:
        name (str): Name of the menu.
        restaurant (Restaurant): The associated restaurant.
        menu_data (dict): JSON field for dishes in menu.
        menu_date (date): The date of the menu. Defaults to the current date.

    Methods:
        __str__(): String representation of the menu.
    """
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_data = models.JSONField()
    menu_date = models.DateField(default=datetime.now().strftime('%Y-%m-%d'))

    def __str__(self):
        return self.name


class Vote(models.Model):
    """
    A vote by a user for a specific menu on a date.

    Fields:
        user (User): Voting user.
        menu (Menu): Voted menu.
        vote_date (date): The date of the vote. Defaults to the current date.

    Meta:
        unique_together (tuple): Ensures the combination of user, menu, and vote date is unique.

    Methods:
        __str__(): String representation of the vote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote_date = models.DateField(default=datetime.now().strftime('%Y-%m-%d'))

    class Meta:
        unique_together = ('user', 'menu', 'vote_date')

    def __str__(self):
        return f"Vote by {self.user.username} for {self.menu.name} on {self.vote_date}."

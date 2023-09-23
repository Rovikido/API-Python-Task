from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_data = models.JSONField()

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote_date = models.DateField()

    class Meta:
        unique_together = ('user', 'menu', 'vote_date')

    def __str__(self):
        return f"Vote by {self.user.username} for {self.menu.name} on {self.vote_date}."
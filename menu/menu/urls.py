from django.contrib import admin
from django.urls import path
from .views import CombinedTokenObtainPairView

from menu import views



urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.register_user, name='user_registration'),

    path('api/token/', CombinedTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('restaurants/get_all_restaurants', views.get_restaurant_list),
    path('restaurants/add_restaurants', views.add_restaurant),

    path('menu/get_all_menus', views.get_all_menus),
    path('menu/get_menus_for_date', views.get_menus_for_date),
    path('menu/get_result_for_date', views.get_result_for_date),
    path('menu/add_restaurants', views.add_restaurant),
    path('menu/add_menu', views.add_menu),

    path('vote', views.vote)
]

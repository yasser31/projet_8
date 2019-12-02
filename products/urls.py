from django.urls import path
from . import views

# products url
urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('save/<int:product_id>', views.save, name="save"),
    path('preferences/', views.preferences, name="preferences"),
    path('remove/<int:preference_id>', views.remove_preferences, 
         name="remove"),
    path('signup/', views.signup, name="signup"),
    path("contact/", views.contact, name="contact"),
    path("legal/", views.legal_notice, name="legal"),
    path("profile/", views.account, name="profile"),
]

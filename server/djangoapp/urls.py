from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path('register/', views.registration, name='registration'),

    # Path for login and logout
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # Path for getting cars
    path('get_cars/', views.get_cars, name='getcars'),

    # Path for dealer reviews
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # Path for adding a review
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review/', views.add_review, name='add_review'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

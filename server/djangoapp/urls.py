# Uncomment the imports before you add the function code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for registration
    path(route='register', view=views.registration, name='registration'),

    # path for login
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # path for dealer reviews view
    path(
        'dealer/<int:dealer_id>',
        views.get_dealer_details,
        name='dealer_details'
    ),
    path(
       'dealer/<int:dealer_id>/review',
        views.add_review,
        name='add_review'
    ),
    path(
        'dealer/<int:dealer_id>/postreview',
        views.post_review,
        name='post_review'
    ),

    # path for add a review view
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name="dealer_details"),
    path(route='add_review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

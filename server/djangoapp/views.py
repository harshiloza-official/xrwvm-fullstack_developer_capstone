from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
    return JsonResponse({"CarModels": cars})

@csrf_exempt
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"error": "Authentication failed"}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def registration(request):
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    
    except KeyError as e:
        return JsonResponse({"error": f"Missing required field: {e}"}, status=400)

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_reviews(request, dealer_id):
    try:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        
        return JsonResponse({"status": 200, "reviews": reviews})
    
    except Exception as e:
        logger.error(f"Error fetching dealer reviews: {e}")
        return JsonResponse({"status": 500, "error": "Internal Server Error"})

def get_dealer_details(request, dealer_id):
    try:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    
    except Exception as e:
        logger.error(f"Error fetching dealer details: {e}")
        return JsonResponse({"status": 500, "error": "Internal Server Error"})

def add_review(request):
    try:
        if request.user.is_authenticated:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 403, "error": "Unauthorized"})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    except Exception as e:
        logger.error(f"Error posting review: {e}")
        return JsonResponse({"status": 500, "error": "Internal Server Error"})

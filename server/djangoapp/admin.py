# Register your models here.
from django.contrib import admin
from .models import CarMake, CarModel
# CarModelInline class

# CarModelAdmin class
admin.site.register(CarMake)
admin.site.register(CarModel)

# CarMakeAdmin class with CarModelInline

# Register models here

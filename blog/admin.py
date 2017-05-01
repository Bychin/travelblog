from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import PlaceSpot
from .models import Post

admin.site.register(Post, LeafletGeoAdmin)
admin.site.register(PlaceSpot, LeafletGeoAdmin)

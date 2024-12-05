from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)

api.add_router("/spy_cats/", "cats.api.router")
api.add_router("/missions/", "missions.api.router")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

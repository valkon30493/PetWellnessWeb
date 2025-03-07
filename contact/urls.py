from django.urls import path
from django.shortcuts import render  # ✅ Add this import
from .views import contact_view

urlpatterns = [
    path("", contact_view, name="contact"),
    path("success/", lambda request: render(request, "contact/contact_success.html"), name="contact_success"),
]



from django.urls import path
from .views import edit_review

urlpatterns = [
    path("edit/<int:review_id>/", edit_review, name="edit_review"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("edit/<int:review_id>/", views.review_edit, name="review_edit"),
    path("delete/<int:review_id>/", views.review_delete, name="review_delete"),
]

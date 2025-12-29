from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.text = request.POST.get("text")
        review.rating = request.POST.get("rating")
        review.save()
        return redirect("event_detail", event_id=review.event.id)

    return render(request, "reviews/edit_review.html", {
        "review": review
    })

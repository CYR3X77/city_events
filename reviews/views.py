from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("event_detail", event_id=review.event.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_edit.html", {
        "form": form,
        "review": review
    })


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    event_id = review.event.id
    review.delete()
    return redirect("event_detail", event_id=event_id)

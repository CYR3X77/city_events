from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from reviews.models import Review
from reviews.forms import ReviewForm


def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/event_list.html', {
        'events': events
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = Review.objects.filter(event=event).order_by('-created_at')

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            event=event,
            user=request.user
        ).first()

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            return redirect("event_detail", event_id=event.id)
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Count
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event, Favorite
from reviews.models import Review
from reviews.forms import ReviewForm


def event_list(request):
    events = Event.objects.all()

    #  Поиск
    query = request.GET.get('q', '').strip()
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    #  Средний рейтинг
    events = events.annotate(
        average_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    )

    #  Сортировка
    sort = request.GET.get('sort', 'date_desc')

    if sort == 'date_asc':
        events = events.order_by('date')
    elif sort == 'title_asc':
        events = events.order_by('title')
    elif sort == 'rating_desc':
        events = events.order_by('-average_rating', '-reviews_count', '-date')
    else:  # date_desc
        events = events.order_by('-date')

    return render(request, 'events/event_list.html', {
        'events': events,
        'query': query,
        'sort': sort,
    })


@login_required
def toggle_favorite(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        event=event
    )

    if created:
        messages.success(request, "💖 Событие добавлено в избранное")
    else:
        favorite.delete()
        messages.info(request, "💔 Событие удалено из избранного")

    return redirect("event_detail", event_id=event.id)


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('event')

    return render(request, 'events/favorites_list.html', {
        'favorites': favorites
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = Review.objects.filter(event=event).order_by('-created_at')

    user_review = None
    is_favorite = False

    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            event=event,
            user=request.user
        ).first()

        is_favorite = Favorite.objects.filter(
            user=request.user,
            event=event
        ).exists()

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()

            messages.success(request, "✅ Отзыв успешно сохранён")
            return redirect("event_detail", event_id=event.id)
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'is_favorite': is_favorite,
    })

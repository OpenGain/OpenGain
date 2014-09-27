from django.contrib import messages
from django.shortcuts import render, redirect
from default_set.reviews.forms import ReviewForm
from .models import Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _


def index(request):
    object_list = Review.objects.filter(is_public=True)
    paginator = Paginator(object_list, 20)

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, _('Ваш отзыв успешно отправлен и будет опубликован после модерации.'))
        return redirect('reviews_index')

    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render(request, 'reviews/index.html',
                  dict(object_list=object_list, form=form)
    )
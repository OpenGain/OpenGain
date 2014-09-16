from django.shortcuts import render, get_object_or_404
from default_set.news.models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    object_list = News.objects.filter(is_public=True)
    paginator = Paginator(object_list, 5)

    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render(request, 'news/index.html', dict(object_list=object_list))


def detail(request, slug):
    object = get_object_or_404(News, slug=slug)
    return render(request, 'news/detail.html', dict(object=object))
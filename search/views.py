# encoding: utf-8
__author__ = 'Nazmi ZORLU'
__email__ = "nazmizorlu@gmail.com"

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache

from search.models import Search
from search.forms import SearchForm


def main(request):
    searches = None
    form = SearchForm()
    phrase = request.GET.get("phrase", None)
    location = request.GET.get("location", None)

    if phrase and location:
        form = SearchForm(request.GET)
        if form.is_valid():
            search, search_created = Search.objects.get_or_create(
                phrase=form.cleaned_data["phrase"],
                location=form.cleaned_data["location"])
            cached_venues = cache.get("venues_%d" % search.pk, None)
            if cached_venues is None:
                search.collect_venues()
                cached_venues = search.venues.all()
                cache.set("venues_%d" % search.pk, cached_venues, timeout=60*60)

            paginator = Paginator(cached_venues, 10)
            page = request.GET.get("page", 1)

            try:
                page = int(page)
            except ValueError:
                page = 1

            try:
                searches = paginator.page(page)
            except EmptyPage:
                searches = None

    return render(request, "main.html",
                  {"form": form,
                   "latest": Search.objects.all()[:20],
                   "results": searches})


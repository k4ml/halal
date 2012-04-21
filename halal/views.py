#-*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.db.models import F

import haystack
from haystack.views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

from halal.models import Product, Keyword
from halal.scrape import search

class ProductSearchView(SearchView):
    form_class = SearchForm

    def __init__(self, *args, **kwargs):
        super(ProductSearchView, self).__init__(self)
        self.form_class = SearchForm
        self.template = 'search.html'

    def __call__(self, request):
        response = super(ProductSearchView, self).__call__(request)
        logger.info('Test logging')

        logger.debug("Total results: %d" % len(self.results))
        if not self.results.count() > 0 and self.query:
            # jakim can only search for single keyword so we only
            # pass the first keyword
            keyword = self.query.split()[0]
            try:
                logger.debug("Searching JAKIM for %s from query:%s" % (keyword, self.query))
                search(keyword) # try getting result from jakim directly
            except Exception as e:
                logger.debug("Failed searching JAKIM exc:%s" % e)
                return response
            else:
                return redirect(self.request.get_full_path())

        logger.debug("Results found")
        kw_obj, kw_created = Keyword.objects.get_or_create(name=self.query)
        if kw_obj and not kw_created:
            kw_obj.count = F('count') + 1
            kw_obj.save()

        return response

    def extra_context(self):
        extra = super(ProductSearchView, self).extra_context()
        qs = Keyword.objects.all().order_by('-modified')
        extra['latest_searches'] = qs[:10]

        return extra

def tmp_result(request):
    context = {}
    simple_backend = haystack.load_backend('simple')
    query = request.GET.get('q', '')
    results = SearchQuerySet().auto_query(query)

    paginator = Paginator(results, 20) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context['query'] = query
    context['page'] = products

    return render(request, 'search.html', context)

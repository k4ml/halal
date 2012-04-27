#-*- coding: utf-8 -*-

# Copyright (c) 2011(s), Mohd. Kamal Bin Mustafa <kamal.mustafa@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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

    def extra_context(self):
        extra = super(ProductSearchView, self).extra_context()
        qs = Keyword.objects.all().order_by('-modified')
        extra['latest_searches'] = qs[:10]
        result_count = self.results.count()

        if self.query:
            kw_obj, kw_created = Keyword.objects.get_or_create(name=self.query)
            if not kw_created:
                kw_obj.count = F('count') + 1

            if result_count == 0 and not kw_obj.scrapped:
                extra['messages'] = 'Dalam process mendapatkan data daripada laman JAKIM. Sila cuba sebentar lagi'
            if result_count == 0 and kw_obj.scrapped:
                extra['messages'] = ''

            kw_obj.save()

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

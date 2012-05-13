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

from django.db import models

class Company(models.Model):
    name = models.TextField()

class Scrap(models.Model):
    url = models.TextField()
    content = models.TextField(blank=True)
    has_result = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Product(models.Model):
    CATEGORY = (
        (1, 'Produk'),
        (2, 'Premis'),
    )
    name = models.TextField()
    expired = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.IntegerField(choices=CATEGORY)
    source = models.ForeignKey(Scrap)

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    scrapped = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.name

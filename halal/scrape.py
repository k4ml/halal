#-*- coding: utf-8 -*-

import os
import sys
import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'halal.local_settings'

import logging
logger = logging.getLogger(__name__)

import requests
import lxml.html

from django.db import transaction

from halal.models import Product, Scrap

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_company(elm):
    modal = None
    try:
        for key, value in elm.cssselect('img')[-1].items():
            if key == 'onclick':
                modal = value
    except Exception:
        pass

    try:
        if modal:
            url = modal[len("openModal('"):]
            return url.split(',')[0]
    except Exception:
        pass

    return 'N/A'

class NoResult(Exception): pass

def parse_product(page_content, scrap_obj):
    root = lxml.html.fromstring(page_content)
    outer_table = root.cssselect("table")[1]
    found = False
    has_result = False
    for tr in outer_table.cssselect("tr"):
        for td in tr.cssselect("td"):
            if td.text_content().strip() == 'SENARAI PRODUK':
                found = True
                break
        if found:
            data_row_counter = 0
            for idx, td in enumerate(tr.cssselect("tr")):
                if idx < 3: continue
                #logger.debug('Row with data found')
                data_row_counter += 1
                row_data = strip_tags(td.text_content()).strip()
                row_data_part = row_data.split('\n')

                try:
                    bil = row_data_part[0].strip()
                    product = row_data_part[2].strip().replace("\t", '')
                    product = ' '.join(product.split()) # remove whitespace
                    expired = row_data_part[5].strip()
                except Exception as e:
                    logger.debug('Failed extracting data exception:%s' % e)
                    continue

                #print bil, product, expired
                logger.debug('Got data product:%s, expired:%s' % (product, expired))
                try:
                    expired_dt = datetime.datetime.strptime(expired, '%d/%m/%Y')
                except Exception as e:
                    logger.debug('Failed getting expired_dt exception:%s' % e)
                    continue

                if Product.objects.filter(name=product).exists():
                    logger.debug("Product already exists - %s" % product)
                    continue

                pobj = Product(name=product, expired=expired_dt, source=scrap_obj)
                pobj.save()
                has_result = True
                #print 'Saved %s' % pobj.name

    if not has_result:
        raise NoResult("No results found")

    scrap_obj.has_result = True
    scrap_obj.save()

@transaction.commit_on_success
def search(keyword):
    logger.debug('Start searching %s' % keyword)
    base_url = 'http://www.halal.gov.my/ehalal'
    url = "%s/directory_standalone.php?type=P&cari=%s" % (base_url, keyword)
    html = requests.get(url).content
    root = lxml.html.fromstring(html)
    found_pages = []
    for aelm in root.cssselect('a'):
        for attr, value in aelm.items():
            if attr == 'href' and value.startswith('directory_standalone.php'):
                found_pages.append(value)
                logger.debug('Found link %s' % value)

    for idx, found_page_url in enumerate(found_pages):
        scrap_obj, created = Scrap.objects.get_or_create(url=url)
        scrap_obj.content = html
        if idx == 0: # we already have the first page
            parse_product(html, scrap_obj)
            continue

        try:
            url = '%s/%s' % (base_url, found_page_url)
            html = requests.get(url).content
            parse_product(html, scrap_obj)
            print 'parsing product from %s' % url
        except Exception as e:
            logger.debug('Failed parsing %s exception:%s' % (url, e))
            continue

if __name__ == '__main__':
    try:
        search(sys.argv[1])
    except Exception as e:
        print e

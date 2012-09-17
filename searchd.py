import os
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'halal.local_settings'

from django.db import transaction

from halal.models import Keyword
from halal.scrape import search

@transaction.commit_on_success
def search_keywords(args):
    print 'Start loop %d' % time.time()
    for keyword in Keyword.objects.filter(scrapped=False):
        keyword_part = keyword.name.split()
        try:
            first_kw = keyword_part[0].strip('"')
            print "Searching for %s" % first_kw
            search(first_kw)
            search(first_kw, 'M')
        except Exception as e:
            print e, keyword

        keyword.scrapped = True
        keyword.save()
        print "Searching for %s done" % keyword_part[0]

    return True

def main(args=None):
    while True:
        search_keywords(args)
        sys.stdout.flush()
        time.sleep(10)

if __name__ == '__main__':
    import signal
    import sys
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    print 'Press Ctrl+C'
    main(sys.argv)

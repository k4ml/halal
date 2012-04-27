import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'halal.local_settings'

from halal.models import Keyword
from halal.scrape import search

def search_keywords(args):
    for keyword in Keyword.objects.filter(scrapped=False):
        keyword_part = keyword.name.split()
        try:
            print "Searching for %s" % keyword_part[0]
            search(keyword_part[0])
        except Exception as e:
            print e
        else:
            keyword.scrapped = True
            keyword.save()

def main(args=None):
    while True:
        search_keywords(args)

if __name__ == '__main__':
    import signal
    import sys
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    print 'Press Ctrl+C'
    main(sys.argv)

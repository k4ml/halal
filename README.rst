Getting Started
===============
Make sure to have ``virtualenv``. On Ubuntu, you can install it through ``sudo apt-get install python-virtualenv``. In the root directory::
    
    $ make virtualenv
    $ make requirements
    $ cp halal/example_local_settings.py halal/local_settings.py
    $ # edit database info in local_settings.py
    $ ./bin/python manage.py syncdb
    $ ./bin/python halal/scrape.py <keyword>
    $ ./bin/manage.py rebuild_index

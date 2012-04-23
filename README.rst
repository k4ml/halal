Live site - http://halal.it.cx/

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
    $ make static # create halal/htdocs dir and run collectstatic command

Deployment
==========
Here's a sample of apache vhost config for deployment with apache using ``mod_wsgi``::

    <VirtualHost *:80>
        ServerName halal.it.cx

        Alias /static /home/kamal/project/halal/halal/htdocs
        <Directory /home/kamal/project/halal/halal/htdocs>
            Order Allow,Deny
            Allow from all
        </Directory>

        WSGIDaemonProcess halal processes=1 threads=10 python-path=/home/kamal/project/halal:/home/kamal/project/halal/lib/python2.7/site-packages
        WSGIProcessGroup halal

        WSGIScriptAlias / /home/kamal/project/halal/halal/wsgi/run.wsgi
    </VirtualHost>

The above assume you checkout the project to ``/home/kamal/project`` when cloning the git repo::

    $ cd /home/kamal/project
    $ git clone git://github.com/k4ml/halal.git

Motivation
==========
https://plus.google.com/u/0/115371258798208681274/posts/cNE4H13kEg7

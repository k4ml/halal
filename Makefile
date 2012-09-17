
virtualenv:
	virtualenv .

requirements:
	while read line; do ./bin/easy_install -U $$line; done < requirements.txt

settings:
	cp halal/example_local_settings.py halal/local_settings.py

static:
	mkdir -p halal/htdocs
	./bin/python manage.py collectstatic

logs:
	mkdir -p halal/logs


virtualenv:
	virtualenv .

requirements:
	while read line; do ./bin/easy_install -U $$line; done < requirements.txt

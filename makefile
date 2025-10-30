BIN=./venv/bin/
sources = apps/


.PHONY: install
i:
	$(BIN)python -m pip install -U pip
	$(BIN)pip install -U -r ./requirements.txt

r:
	$(BIN)python ./manage.py runserver 0.0.0.0:8000 --verbosity 0

m:
	$(BIN)python ./manage.py migrate

mm:
	$(BIN)python ./manage.py makemigrations

s:
	$(BIN)python ./manage.py shell

newapp:
	$(BIN)python ./manage.py startapp $(name)

compile:
	$(BIN)python ./manage.py compilemessages
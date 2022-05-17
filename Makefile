bacen: requisitos.txt
	pip install -r requisitos.txt
	npm install -g @angular/cli
	python3 python/flaskServer.py &
	(cd angular; npm install; ng serve)

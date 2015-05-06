clean:
	@find . -name "*.pyc" -delete

deps: clean
	@pip install -r test-requirements.txt

test: deps
	@./manage.py test
	@flake8 .

run: deps
	@./manage.py runserver

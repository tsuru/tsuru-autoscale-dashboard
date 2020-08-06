clean:
	@find . -name "*.pyc" -delete

deps: clean
	@pip install -r test-requirements.txt

test: deps
	@./manage.py test
	@flake8 --max-line-length 150 .

run: deps
	@./manage.py runserver

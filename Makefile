clean:
	@find . -name "*.pyc" --delete

deps: clean
	@pip install -r requirements.txt

test: deps
	@./manage.py test

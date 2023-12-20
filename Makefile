
push:
	git add .
	git commit -m "update"
	git push --set-upstream origin master

dev:
	poetry run python main.py

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "__pycache__" -exec rm -rf {} \;
	find . -name ".pytest_cache" -exec rm -rf {} \;
	find . -name ".DS_Store" -exec rm -rf {} \;
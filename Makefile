build:
	find . -name __pycache__ -type d -exec rm -rv {} + && rm -rf build.zip && zip -r build.zip application requirements.txt

build: build_frontend build_serverless

build_frontend:
	rm -rf ./out
	rm -rf ./arrive
	yarn --cwd skills-search-tram-frontend postbuild
	yarn --cwd skills-search-tram-frontend build
	cd skills-search-tram-frontend && zip -r ../arrive.zip out

build_serverless:
	find . -name __pycache__ -type d -exec rm -rv {} +
	rm -rf build.zip
	zip -r build.zip application requirements.txt

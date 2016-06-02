
.PHONY: build clean build-test

build: clean check-env get-version
	docker build -t $(REGISTRY)/marathon_autoscaler:$(VERSION) .

build-test:
	cd tests/stress_test_app && docker build -t $(REGISTRY)/stress_test_app .

check-env:
ifndef REGISTRY
  $(error REGISTRY is undefined)
endif

clean:
	rm -rf ./build

deploy: build
	docker push $(REGISTRY)/marathon_autoscaler:$(VERSION)

get-version:
VERSION=`python -c "import os, sys; sys.path.append(os.path.abspath('lib/marathon-autoscaler')); from constants import __version__; print(__version__)"`
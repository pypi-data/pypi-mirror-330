help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean        to delete files having pattern (*.pyc | *.pyo | *~)"
	@echo "  test         to run the complete set of tests"
	@echo "  test-report  to run the complete set of tests and generate test and coverage reports"

clean:
	find . -name '*.pyc' -exec rm --force {} \;
	find . -name '*.pyo' -exec rm --force {} \;
	find . -name '*~' -exec rm --force {} \;
	find . -name '__pycache__' -exec rm -r --force {} \;
	find . -name '.pytest_cache' -exec rm -r --force {} \;

test:
	make clean
	pytest -ra -q

test-report:
	make clean
	pytest -ra -q --html=tests/html/report.html --cov=melospy_web --cov=pattern_search --cov-report html:tests/coverage


# docker_image_base_name = docker.io/kqmqneyosi8e/test-delete
# docker_image_base_name = registry.gitlab.com/computational-audition/experiment-images

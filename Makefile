STAGE ?= dev
VIRTUAL_ENV ?= venv
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_ROOT_DIR := $(dir $(MAKEFILE_PATH))
PYTHON_RUNTIME ?= python3

APP_CONFIG_FILE ?= ${PROJECT_ROOT_DIR}configs/app/${STAGE}/config.yml

clean:
	rm -rf ${VIRTUAL_ENV}

python-venv:
	${PYTHON_RUNTIME} -m venv ${VIRTUAL_ENV}
	. ${VIRTUAL_ENV}/bin/activate && \
	${PYTHON_RUNTIME} -m pip install -r requirements-base.txt && \
	${PYTHON_RUNTIME} -m pip install -r requirements-dev.txt

analyze:
	. ${VIRTUAL_ENV}/bin/activate && \
	bash ${PROJECT_ROOT_DIR}scripts/analyze.sh -d "src scripts tests" -t tests

test:
	APP_CONFIG_FILE=${APP_CONFIG_FILE} \
	. ${VIRTUAL_ENV}/bin/activate && \
	pytest -vv ${TEST_TAG_PARAM} --junit-xml xunit.xml --cov src --cov-report xml tests/unit && \
	diff-cover coverage.xml --fail-under=50

app-offline:
	. ${VIRTUAL_ENV}/bin/activate && \
	PROJECT_ROOT_DIR=${PROJECT_ROOT_DIR} \
	APP_CONFIG_FILE=${APP_CONFIG_FILE} \
	python ${PROJECT_ROOT_DIR}src/manager.py

e2e-test:
	. ${VIRTUAL_ENV}/bin/activate && \
	APP_CONFIG_FILE=${APP_CONFIG_FILE} \
	TEST_TAG=${TEST_TAG} \
	ENDPOINT_BASE_URL=${ENDPOINT_BASE_URL} \
	bash ${PROJECT_ROOT_DIR}scripts/run_e2e_tests.sh

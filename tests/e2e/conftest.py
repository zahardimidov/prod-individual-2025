import logging
from collections.abc import MutableMapping
from typing import Any
import pytest
import time
import subprocess
from dotenv import find_dotenv

docker_compose_file = find_dotenv('test-docker-compose.yml')

@pytest.fixture(scope='session', autouse=True)
def setup_session():
    try:
        cmd = f"docker compose -f {docker_compose_file} up --build -d"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)

        if result.returncode != 0:
            logging.critical(f"Failed to start Docker Compose: {result.stderr}")
            pytest.exit("Docker Compose failed to start")
        time.sleep(5)
        yield
    finally:
        cmd = f'docker compose -f {docker_compose_file} down'
        result = subprocess.run(cmd.split(), capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f"Docker Compose failed to stop: {result.stderr}")
        else:
            logging.info('Docker Compose stoped')

def pytest_tavern_beta_before_every_request(request_args: MutableMapping):
    message = f"Request: {request_args['method']} {request_args['url']}"

    params = request_args.get('params', None)
    if params:
        message += f"\nQuery parameters: {params}"
    
    message += f"\nRequest body: {request_args.get('json', '<no body>')}"

    logging.info(message)

def pytest_tavern_beta_after_every_response(expected: Any, response: Any) -> None:
    logging.info(f"Response: {response.status_code} {response.text}")
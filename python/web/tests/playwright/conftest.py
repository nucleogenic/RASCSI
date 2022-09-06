import pytest

@pytest.fixture(scope="function", autouse=True)
def set_httpserver_hostname(httpserver):
    # The HTTP requests are made by Python from within the container so we need
    # httpserver.url_for to generate URLs which point to the Docker host
    httpserver.host = "host.docker.internal"

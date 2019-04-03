# coding: utf-8

import pytest
import app as service
import yaml
import responder
from starlette.responses import PlainTextResponse


@pytest.fixture
def api():
    return service.api


def test_hello_world(api):
    r = api.requests.get("/api/v1.0/index")
    assert r.text == "Hello, World!"


def test_basic_route(api):
    @api.route("/api/v1.0/index")
    def index(req, resp):
        resp.text = "Hello, World!"


def test_requests_session(api):
    assert api.session()
    assert api.requests


def test_json_media(api):
    dump = {"life": 42}

    @api.route("/")
    def media(req, resp):
        resp.media = dump

    r = api.requests.get("http://;/")

    assert "json" in r.headers["Content-Type"]
    assert r.json() == dump


def test_yaml_media(api):
    dump = {"life": 42}

    @api.route("/")
    def media(req, resp):
        resp.media = dump

    r = api.requests.get("http://;/", headers={"Accept": "yaml"})

    assert "yaml" in r.headers["Content-Type"]
    assert yaml.load(r.content) == dump


def test_background(api):
    @api.route("/")
    def route(req, resp):
        @api.background.task
        def task():
            import time
            time.sleep(3)

        task()
        api.text = "ok"

    r = api.requests.get(api.url_for(route))
    assert r.ok


def test_500_error(api):
    def catcher(req, exc):
        return PlainTextResponse("Suppressed error", 500)

    api.app.add_exception_handler(ValueError, catcher)

    @api.route("/api/v1.0/index")
    def view(req, resp):
        raise ValueError

    r = api.requests.get(api.url_for(view))
    assert not r.ok
    assert r.content == b'Suppressed error'


def test_404_error(api):
    r = api.requests.get("/api/v1.0/foo")

    assert r.status_code == responder.API.status_codes.HTTP_404

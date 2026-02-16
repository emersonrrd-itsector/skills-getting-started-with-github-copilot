import copy
from fastapi.testclient import TestClient
from src import app as app_module
from src.app import app

client = TestClient(app)


def setup_function(function):
    # backup activities before each test
    function._activities_backup = copy.deepcopy(app_module.activities)


def teardown_function(function):
    # restore activities after each test
    app_module.activities.clear()
    app_module.activities.update(function._activities_backup)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: Chess Club should exist
    assert "Chess Club" in data


def test_signup_and_duplicate():
    activity = "Chess Club"
    email = "teststudent@example.com"

    # ensure email not already present
    assert email not in app_module.activities[activity]["participants"]

    # sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # duplicate signup should be rejected
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_remove_participant():
    activity = "Programming Class"
    email = "toremove@example.com"

    # add participant first
    client.post(f"/activities/{activity}/signup?email={email}")
    assert email in app_module.activities[activity]["participants"]
import copy
from fastapi.testclient import TestClient
from src import app as app_module
from src.app import app

client = TestClient(app)


def setup_function(function):
    # backup activities before each test
    function._activities_backup = copy.deepcopy(app_module.activities)


def teardown_function(function):
    # restore activities after each test
    app_module.activities.clear()
    app_module.activities.update(function._activities_backup)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: Chess Club should exist
    assert "Chess Club" in data


def test_signup_and_duplicate():
    activity = "Chess Club"
    email = "teststudent@example.com"

    # ensure email not already present
    assert email not in app_module.activities[activity]["participants"]

    # sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # duplicate signup should be rejected
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_remove_participant():
    activity = "Programming Class"
    email = "toremove@example.com"

    # add participant first
    client.post(f"/activities/{activity}/signup?email={email}")
    assert email in app_module.activities[activity]["participants"]

    # remove participant
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_remove_nonexistent_participant():
    activity = "Gym Class"
    email = "nonexistent@example.com"

    assert email not in app_module.activities[activity]["participants"]
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
import json
import requests
import helpers

config = json.load(open("appsettings.json"))
PATH = config["PATH"]
USER = config["USER"]
PASS = config["PASS"]
PLAYERS_PER_PAGE = config["PLAYERS_PER_PAGE"]


def test_number_of_players_per_page():
    print("-----------Test started-------------")
    print("Verify that each request returns exact {0} players details".format(PLAYERS_PER_PAGE))
    for i in range(1, 101):
        response = helpers.send_request(PATH, USER, PASS, i)
        assert 200 <= response.status_code < 300
        assert len(response.json()) == PLAYERS_PER_PAGE


def test_id_range_of_players_on_page():
    print("-----------Test started-------------")
    print("Verify that each request contains {0} sequential player's ids ".format(PLAYERS_PER_PAGE))
    for i in range(1, 101):
        response = helpers.send_request(PATH, USER, PASS, i)
        assert 200 <= response.status_code < 300
        assert helpers.validate_sequential_ids(i, response.json(), 1 + (i - 1) * PLAYERS_PER_PAGE,
                                               PLAYERS_PER_PAGE + (i - 1) * PLAYERS_PER_PAGE)


def test_names_of_players_on_page():
    print("-----------Test started-------------")
    print("Verify that all player's names are valid")
    for i in range(1, 101):
        response = helpers.send_request(PATH, USER, PASS, i)
        assert 200 <= response.status_code < 300
        assert helpers.validate_names(i, response.json())


def test_navigate_to_page_with_hop():
    print("-----------Test started-------------")
    print("Verify that players details are valid, when navigate to specific page")
    for i in range(2, 101, 3):
        response = helpers.send_request(PATH, USER, PASS, i)
        assert 200 <= response.status_code < 300
        assert len(response.json()) == PLAYERS_PER_PAGE
        assert helpers.validate_sequential_ids(i, response.json(), 1 + (i - 1) * PLAYERS_PER_PAGE,
                                               PLAYERS_PER_PAGE + (i - 1) * PLAYERS_PER_PAGE)
        assert helpers.validate_names(i, response.json())


def test_unauthorized_user():
    print("-----------Test started-------------")
    print("Verify that unauthorized user got code 400")
    response = requests.get(PATH + "{0}".format(1))
    print("Get {0}".format(PATH + "{0}".format(1)))
    assert response.status_code >= 400


def test_wrong_pass():
    print("Verify that user with wrong password got code 400")
    response = helpers.send_request(PATH, USER, "PASS", 1)
    assert response.status_code >= 400


def test_wrong_user():
    print("Verify that user with wrong username got code 400")
    response = helpers.send_request(PATH, "USER", PASS, 1)
    assert response.status_code >= 400


def test_invalid_page_id_number():
    print("Verify that request with invalid page got code 400")
    response = helpers.send_request(PATH, USER, PASS, 0)
    assert response.status_code >= 400


def test_invalid_page_id_string():
    print("Verify that request with invalid path got code 400")
    response = helpers.send_request(PATH, USER, PASS, "*")
    assert response.status_code >= 400


def test_sql_injection():
    print("Verify that request with sql injection got code 400")
    response = helpers.send_request(PATH, USER, PASS, "1; DROP TABLE players;")
    assert response.status_code >= 400

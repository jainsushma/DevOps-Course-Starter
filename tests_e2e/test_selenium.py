import pytest
import os
import requests
import time
from threading import Thread
import todo_app.app as app
from selenium import webdriver
from selenium.webdriver import Firefox

# Install the driver:
# Downloads the latest GeckoDriver version
# Adds the downloaded GeckoDriver to path
# get_driver = GetGeckoDriver()
# get_driver.install()

# Use the installed GeckoDriver with Selenium
# driver = webdriver.Firefox()
# driver.get("https://google.com")
# time.sleep(3)
# driver.quit()


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    board_id = create_trello_board("Test Board")
    os.environ['BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)

def create_trello_board(name):
    params = {"key": os.getenv('SECRET_KEY'),
              "token": os.getenv('TOKEN'), "name": name}
    response = requests.post(
        f"https://api.trello.com/1/boards/", params=params)
    return response.json()["id"]
             

def delete_trello_board(id):
    params = {"key": os.getenv('SECRET_KEY'),
              "token": os.getenv('TOKEN'),}
    response = requests.delete(
        f"https://api.trello.com/1/boards/{id}", params=params)
    return response

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
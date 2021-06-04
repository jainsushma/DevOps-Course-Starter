import pytest
import os
import requests
import time
from threading import Thread
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from selenium import webdriver
from selenium.webdriver import Firefox

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
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
    time.sleep(3)
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

    # Create a task
    driver.find_element_by_id("title").send_keys("New Item")
    # driver.find_element_by_xpath("//a[contains(text(),'Add Item')]").click()
    driver.find_element_by_id("addItem").click()
    time.sleep(5)
    # verify if the task is in To Do list
    value = driver.find_element_by_id("To-Do-Items")
    time.sleep(2)
    assert "New Item" in value.text
    
    # Move task to Doing list
    driver.find_element_by_xpath("//a[contains(text(),'Start')]").click()
    time.sleep(5)

    # Verify if the task is in Doing list
    value = driver.find_element_by_id("Doing-Items")
    time.sleep(2)
    assert "New Item" in value.text

    # Move task to Done list
    driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
    time.sleep(5)

    # Verify if the task is in Done list
    value = driver.find_element_by_id("Done-Items")
    time.sleep(2)
    assert "New Item" in value.text

    # Move task to To Do list again
    driver.find_element_by_xpath("//a[contains(text(),'Mark as Incomplete')]").click()
    time.sleep(5)

    # Verify if the task is in To Do list
    value = driver.find_element_by_id("To-Do-Items")
    time.sleep(2)
    assert "New Item" in value.text

    # Delete the task
    driver.find_element_by_xpath("//a[contains(text(),'Delete')]").click()
    time.sleep(5)

    # Verify if the task is deleted
    value = driver.find_element_by_id("To-Do-Items")
    time.sleep(2)
    assert "New Item" not in value.text
    # driver.quit()
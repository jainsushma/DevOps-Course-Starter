import pytest
import os
import requests
import time
from threading import Thread
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from todo_app.mongo_actions import MongoActions
import pymongo
from selenium import webdriver
        
@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    os.environ['DBNAME'] = "TODOSELENIUMDB"
    os.environ['LOGIN_DISABLED'] = "True"
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
    MongoActions().client.drop_database("TODOSELENIUMDB", session=None)

def test_task_journey(driver, app_with_temp_board):
    driver.implicitly_wait(5)
    time.sleep(3)
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    # Create a task
    driver.find_element_by_id("title").send_keys("New Item")
    # driver.find_element_by_xpath("//a[contains(text(),'Add Item')]").click()
    driver.find_element_by_id("addItem").click()
    # verify if the task is in To Do list
    value = driver.find_element_by_id("ToDoItems")
    assert "New Item" in value.text
    
    # Move task to Doing list
    driver.find_element_by_xpath("//*[contains(text(),'Start')]").click()

    # Verify if the task is in Doing list
    value = driver.find_element_by_id("DoingItems")
    assert "New Item" in value.text

    # Move task to Done list
    driver.find_element_by_xpath("//*[contains(text(),'Complete')]").click()

    # Verify if the task is in Done list
    value = driver.find_element_by_id("DoneItems")
    assert "New Item" in value.text

    # Move task to To Do list again
    driver.find_element_by_xpath("//*[contains(text(),'Mark as Incomplete')]").click()

    # Verify if the task is in To Do list
    value = driver.find_element_by_id("ToDoItems")
    assert "New Item" in value.text

    # Delete the task
    driver.find_element_by_xpath("//*[contains(text(),'Delete')]").click()

    # Verify if the task is deleted
    value = driver.find_element_by_id("ToDoItems")
    assert "New Item" not in value.text
    # driver.quit()
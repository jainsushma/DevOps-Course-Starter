import pytest, os
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import patch, Mock
import mongomock
import pymongo
       
@pytest.fixture 
def client():
    file_path = find_dotenv('.env.test') 
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)): 
        test_app = app.create_app()
        with test_app.test_client() as client:
            setup_testdata()
            yield client

def setup_testdata():
    db_connection = os.getenv('CLIENT')
    db_name = os.getenv('DBNAME')
    connection = pymongo.MongoClient(db_connection)
    db = connection[db_name]
    card = {"name": "test1", "status": "To Do"}
    collection = db['items']
    collection.insert_one(card)
    
def test_index_page(client):
    # Replace call to requests.get(url) with our own function
    response = client.get('/')
    assert response.status_code == 200
    assert "test1" in str(response.data)


    


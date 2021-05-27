import pytest
import os
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client: 
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    print(response.status)

def mock_get_lists(url, params):
    if url == f'https://api.trello.com/1/boards/{os.getenv("BOARD_ID")}/lists?cards=open&key={os.getenv("SECRET_KEY")}&token={os.getenv("TOKEN")}': 
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_lists_response
        return response
    return None

def sample_trello_lists_response():
    return [
        {
            "id": "doing-1234",
            "name": "doing",
            "idBoard": "test_board",
            "cards": []
        },
        {
            "id": "done-1234",
            "name": "done",
            "idBoard": "test_board",
            "cards": []
        },
        {
            "id": "to-do-1234",
            "name": "to-do",
            "idBoard": "test_board",
            "cards": []
        }
    ]
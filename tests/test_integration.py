import pytest, os
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
    print(response.data.decode())
    assert response.status_code == 200
    assert "To-Do App" in response.data.decode()
    assert "test1" in response.data.decode()
    

def mock_get_lists(url, params=None):
    if url == f'https://api.trello.com/1/boards/{os.getenv("BOARD_ID")}/lists': 
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_lists_response()
        return response
    return None

def sample_trello_lists_response():
    return [
        {
            "id": "doing-1234",
            "name": "Doing",
            "idBoard": "test_board",
            "cards": [
                {
                "id": "1",
                "name": "test1",
                }

            ]
        },
        {
            "id": "Done-1234",
            "name": "Done",
            "idBoard": "test_board",
            "cards": [
                {
                "id": "1",
                "name": "test2",
                }
            ]
        },
        {
            "id": "To-Do-1234",
            "name": "To Do",
            "idBoard": "test_board",
            "cards": [
                {
                "id": "1",
                "name": "test3",
                }
            ]
        }
    ]
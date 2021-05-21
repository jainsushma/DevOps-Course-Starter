import os
import requests
from todo_app.item import Item

class Trello_Board_Actions:
    " Trello util to get lists on a board, get cards and their statuses, update/delete a card"    

    def __init__(self):
        self.auth = {'key':os.getenv("SECRET_KEY"), 'token':os.getenv("TOKEN"), 'cards':"open"}
        self.url= "https://api.trello.com/1"
        self.headers = {
            'type': "type",
            'content-type': "application/json"
                }

    def getBoardLists(self):
        "Get the lists for a given board id"
        board_lists = requests.get(url=self.url + '/boards/' + os.getenv('BOARD_ID') +'/lists', params=self.auth)
        return board_lists.json()

    def getCards(self):
        "Get the card on a list and its status"
        board_lists = Trello_Board_Actions.getBoardLists(self)
        items = []
        for list in board_lists:
            for card in list["cards"]:
                card = Item(
                            card["id"], 
                            card["name"], 
                            list["name"]
                            )
                items.append(card)
        return items
    
    def get_items(self):
        "Simple attempt to get all cards from Trello."
        response = requests.get(f"https://api.trello.com/1/boards/{os.getenv('BOARD_ID')}/cards", params=self.auth)
        todos = response.json()
        return todos

    def addNewCard(self, title):
        "Add a new card on the board"
        result_flag = False
        self.payload = self.auth.copy()
        self.payload['name'] = title
        self.payload['idList'] = Trello_Board_Actions.getListIdByName(self, "to-do")
        response = requests.post(url=self.url + "/cards", data=self.payload)
        if response.status_code == 200:
            result_flag = True
        return result_flag

    def getListIdByName(self,list_name):
        "Get the list id"
        lists_on_board = Trello_Board_Actions.getBoardLists(self)
        for i in range(len(lists_on_board)):
            if lists_on_board[i]['name'] == list_name:
                list_id = lists_on_board[i]['id']
        return list_id 

    def isCardOnList(self, list_name, card_id):
        "Check if the card is on given list name"
        cards_on_the_list = requests.get(url=self.url + '/lists/' + Trello_Board_Actions.getListIdByName(self, list_name) + '/cards', params=self.auth)
        cards_on_the_list = cards_on_the_list.json()
        for i in range(len(cards_on_the_list)):
            if cards_on_the_list[i]['id'] == card_id:
                return True
        return False

    def deleteCard(self, card_id):
        "Delete any card"
        result_flag = False
        response = requests.delete(url=self.url + '/cards/' + card_id, params=self.auth)
        if response.status_code == 200:
            result_flag = True
        return result_flag

    def updateCardStatus(self, id):
        "Update card status"
        result_flag = False
        new_list_id = 0
        if Trello_Board_Actions.isCardOnList(self, "to-do", id):
            new_list_id = Trello_Board_Actions.getListIdByName(self, "doing")
        elif Trello_Board_Actions.isCardOnList(self, "doing", id):
            new_list_id = Trello_Board_Actions.getListIdByName(self, "done")
        else:
            new_list_id = Trello_Board_Actions.getListIdByName(self, "to-do")
       
        self.payload = self.auth.copy()
        self.payload['idList'] = new_list_id
        response = requests.put(url=self.url + '/cards/' + id, data=self.payload)
        if response.status_code == 200:
            result_flag = True

        return result_flag

        
    

    
   
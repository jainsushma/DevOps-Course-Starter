import os
import requests
from todo_app.item import Item

class TrelloBoardActions:
    " Trello util to get lists on a board, get cards and their statuses, update/delete a card"    

    def __init__(self):
        self.auth = {'key':os.getenv("SECRET_KEY"), 'token':os.getenv("TOKEN"), 'cards':"open"}
        self.url= "https://api.trello.com/1"

    def get_board_lists(self):
        "Get the lists for a given board id"
        board_lists = requests.get(url=self.url + '/boards/' + os.getenv('BOARD_ID') +'/lists', params=self.auth)
        return board_lists.json()

    def get_cards(self):
        "Get the card on a list and its status"
        board_lists = self.get_board_lists()
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

    def add_new_card(self, title):
        "Add a new card on the board"
        result_flag = False
        self.payload = self.auth.copy()
        self.payload['name'] = title
        self.payload['idList'] = self.get_list_id_by_name("to-do")
        response = requests.post(url=self.url + "/cards", data=self.payload)
        if response.status_code == 200:
            result_flag = True
        return result_flag

    def get_list_id_by_name(self,list_name):
        "Get the list id"
        lists_on_board = self.get_board_lists()
        for list in lists_on_board:
            if list['name'] == list_name:
                return list['id']
        return None 

    def is_card_on_list(self, list_name, card_id):
        "Check if the card is on given list name"
        cards_on_the_list = requests.get(url=self.url + '/lists/' + self.get_list_id_by_name(list_name) + '/cards', params=self.auth)
        cards_on_the_list = cards_on_the_list.json()
        for card in (cards_on_the_list):
            if card['id'] == card_id:
                return True
        return False

    def delete_card(self, card_id):
        "Delete any card"
        result_flag = False
        response = requests.delete(url=self.url + '/cards/' + card_id, params=self.auth)
        if response.status_code == 200:
            result_flag = True
        return result_flag

    def update_card_status(self, id):
        "Update card status"
        result_flag = False
        new_list_id = 0
        if self.is_card_on_list("to-do", id):
            new_list_id = self.get_list_id_by_name("doing")
        elif self.is_card_on_list("doing", id):
            new_list_id = self.get_list_id_by_name("done")
        else:
            new_list_id = self.get_list_id_by_name("to-do")
       
        self.payload = self.auth.copy()
        self.payload['idList'] = new_list_id
        response = requests.put(url=self.url + '/cards/' + id, data=self.payload)
        if response.status_code == 200:
            result_flag = True

        return result_flag

        
    

    
   
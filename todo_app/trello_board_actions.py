import os
import requests

class Trello_Board_Actions:
    " Trello util to get lists on a board, get the cards and their statuses"    

    def __init__(self):
        self.auth = {'key':os.getenv("SECRET_KEY"), 'token':os.getenv("TOKEN"), 'cards':"open"}
        self.url= "https://api.trello.com/1"
        self.headers = {
            'type': "type",
            'content-type': "application/json"
                }

    def getBoardLists(self):
        "Get the lists for a board id"
        board_list_url = self.url + '/boards/' + os.getenv('BOARD_ID') +'/lists'
        board_lists = requests.get(url=board_list_url,params=self.auth)
        return board_lists.json()

    def getCardsWithStatus(self):
        "Get the card on a list and its status"
        board_lists = Trello_Board_Actions.getBoardLists(self)
        items = []
        for list in board_lists:
            for card in list["cards"]:
                items.append({"id":card['id'],"title":card['name'], "status":list['name']})
        return items

    def addNewCard(self, title):
        "Add a new card on the board"
        result_flag = False
        items = Trello_Board_Actions.getBoardLists(self)
        self.payload = self.auth.copy()
        self.payload['name'] = title
        self.payload['idList'] = items[0]["cards"][0]["idList"]
        add_new_card_url = self.url + "/cards"

        response = requests.post(url=add_new_card_url,data=self.payload)
        if response.status_code == 200:
            result_flag = True

        return result_flag
    
    def getCardIdByName(self,card_name):
        "Get the card id"
        card_id = None
        card_url = self.url + '/boards/' + os.getenv('BOARD_ID') +'/cards'
        card_details = requests.get(url=card_url,params=self.auth)
        card_details = card_details.json()
        for i in range(len(card_details)):
            if card_details[i]['name'] == card_name:
                card_id = card_details[i]['id']
        return card_id 

    def getListIdByName(self,list_name):
        "Get the list id"
        lists_on_board = Trello_Board_Actions.getBoardLists(self)
        for i in range(len(lists_on_board)):
            if lists_on_board[i]['name'] == list_name:
                list_id = lists_on_board[i]['id']
        return list_id 

    def isCardOnList(self, list_name, card_id):
        list_id = Trello_Board_Actions.getListIdByName(self, list_name)
        list_url = self.url + '/boards/' + os.getenv('BOARD_ID') +'/'+ list_id + '/cards'
        cards_on_the_list = requests.get(url=list_url,params=self.auth)
        for i in range(len(cards_on_the_list)):
            if cards_on_the_list[i]['id'] == card_id:
                return True
        return False

    def changeCardStatus(self, id):
        "Change card status"
        result_flag = False
        new_list_id = Trello_Board_Actions.getListIdByName(self, "done")
        update_list_url = self.url + '/cards' + id
        self.payload = self.auth.copy()
        self.payload['idList'] = new_list_id
        if Trello_Board_Actions.isCardOnList(self, "doing", id):
            response = requests.put(url=update_list_url,data=self.payload)
            if response.status_code == 200:
                result_flag = True

        return result_flag

        
    

    
   
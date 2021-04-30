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
        card_lists = Trello_Board_Actions.getBoardLists(self)
        items = []
        for list in card_lists:
            for card in list["cards"]:
                items.append({"title":card["name"], "status":card["closed"]})
        return items
   
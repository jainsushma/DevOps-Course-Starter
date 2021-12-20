import pymongo, os
from todo_app.item import Item
from bson.objectid import ObjectId

class MongoActions:
    " MongoDB utils to get lists on a board, get cards and their statuses, update/delete a card"    

    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("CLIENT"))
        self.db = self.client[os.getenv("DBNAME")]
        self.collection = self.db['items']

    def get_board_lists(self):
        "Get the lists for a given board id"
        board_lists = self.db.list_collection_names()
        return board_lists

    def get_cards(self):
        "Get the card on a list and its status"
        cards = []
        for card in self.collection.find():
            card = Item(
                        card["_id"], 
                        card["name"], 
                        card["status"]
                        )
            cards.append(card)
        return cards

    def add_new_card(self, title):
        "Add a new card on the board"
        card = {"name": title, "status": "To Do"}
        self.collection.insert_one(card)               

    def is_card_on_list(self, card_id):
        "Check if the card is on given list name"
        cards_on_the_list = self.collection.find_one({"_id": ObjectId(card_id)})
        for card in (cards_on_the_list):
            if card['id'] == card_id:
                return True
        return False

    def delete_card(self, card_id):
        "Delete any card"
        output = self.collection.delete_one({"_id": ObjectId(card_id)})
        return output

    def update_card_status(self, id):
        "Update card status"
        card = self.collection.find_one({"_id": ObjectId(id)})
        if card['status'] == "To Do":
            new_card_status = "Doing"
        elif card['status'] == "Doing":
            new_card_status = "Done"    
        else:
            new_card_status = "To Do"
        self.collection.update_one({"_id": ObjectId(id)}, {"$set":{"status": new_card_status}})       
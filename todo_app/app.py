from flask import Flask, render_template, request, redirect
from todo_app.data import session_items
import os
import requests

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def get_items():
    # items = session_items.Session_Items(os.getenv("SECRET_KEY"), os.getenv("TOKEN"))
    auth = {"key":os.getenv("SECRET_KEY"), "token":os.getenv("TOKEN"), "cards":"open"}
    card_lists = requests.get(f"https://api.trello.com/1/boards/{os.getenv('BOARD_ID')}/lists", params=auth).json()
    # items.get_todoItems(os.getenv("SECRET_KEY"), os.getenv("TOKEN"))
    print(card_lists)
    items = []
    for list in card_lists:
        for card in list["cards"]:
            items.append({"title":card["name"], "status":card["closed"]})

    return render_template("index.html", items=items)

@app.route('/add_item', methods=['POST'])
def add_new_item():
    title = request.form['title']
    session_items.add_item(title)
    return redirect(os.getenv("TODO_HOSTNAME"))
   

if __name__ == '__main__':
    app.run(key=os.getenv("SECRET_KEY"),token=os.getenv("TOKEN"))

from flask import Flask, render_template, request, redirect
from todo_app.data import session_items
from todo_app.trello_board_actions import Trello_Board_Actions
import os
import requests

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def get_items():
    lists_on_board = Trello_Board_Actions().getBoardLists()
    print(lists_on_board)
    return render_template("index.html", items=Trello_Board_Actions().getCardsWithStatus())

@app.route('/add_item', methods=['POST'])
def add_new_item():
    title = request.form['title']
    session_items.add_item(title)
    return redirect(os.getenv("TODO_HOSTNAME"))
   

if __name__ == '__main__':
    app.run(key=os.getenv("SECRET_KEY"),token=os.getenv("TOKEN"))

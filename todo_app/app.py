from flask import Flask, render_template, request, redirect, url_for
from todo_app.trello_board_actions import Trello_Board_Actions
import os
import requests

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def get_items():
    return render_template("index.html", items=Trello_Board_Actions().getCards())

@app.route('/add_item', methods=['POST'])
def add_new_item():
    title = request.form['title']
    Trello_Board_Actions().addNewCard(title)
    return redirect(os.getenv("TODO_HOSTNAME"))

@app.route('/move_item/<id>', methods=['POST'])
def move_item(id):
    Trello_Board_Actions().updateCardStatus(id)
    return redirect(os.getenv("TODO_HOSTNAME"))

@app.route('/delete_item/<id>', methods=['POST'])
def delete_item(id):
    Trello_Board_Actions().deleteCard(id)
    return redirect(os.getenv("TODO_HOSTNAME"))

if __name__ == '__main__':
    app.run()

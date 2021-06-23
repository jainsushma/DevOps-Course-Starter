from flask import Flask, render_template, request, redirect, url_for
from todo_app.trello_board_actions import TrelloBoardActions
from todo_app.view_model import ViewModel
import os
import requests

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def get_items():
        return render_template("index.html", model=ViewModel(TrelloBoardActions().get_cards()))

    @app.route('/add_item', methods=['POST'])
    def add_new_item():
        title = request.form['title']
        TrelloBoardActions().add_new_card(title)
        return redirect(os.getenv("TODO_HOSTNAME"))

    @app.route('/move_item/<id>', methods=['POST'])
    def move_item(id):
        TrelloBoardActions().update_card_status(id)
        return redirect(os.getenv("TODO_HOSTNAME"))

    @app.route('/delete_item/<id>', methods=['POST'])
    def delete_item(id):
        TrelloBoardActions().delete_card(id)
        return redirect(os.getenv("TODO_HOSTNAME"))

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from todo_app.view_model import ViewModel
import os
import requests
from todo_app.mongo_actions import MongoActions

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def get_items():
        return render_template("index.html", model=ViewModel(MongoActions().get_cards()))

    @app.route('/add_item', methods=['POST'])
    def add_new_item():
        title = request.form['title']
        MongoActions().add_new_card(title)
        return redirect('/')

    @app.route('/move_item/<id>', methods=['POST'])
    def move_item(id):
        MongoActions().update_card_status(id)
        return redirect('/')

    @app.route('/delete_item/<id>', methods=['POST'])
    def delete_item(id):
        MongoActions().delete_card(id)
        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

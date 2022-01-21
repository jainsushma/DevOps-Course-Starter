from flask import Flask, render_template, request, redirect, url_for
from todo_app.view_model import ViewModel
import os
import requests
from todo_app.mongo_actions import MongoActions
from flask_login import LoginManager, login_required, login_user, UserMixin, current_user
from oauthlib.oauth2 import WebApplicationClient
from functools import wraps

class User(UserMixin):
    def __init__(self, userId):
        self.id = userId
        if userId == 'jainsushma':
            self.role = "writer"
        else: 
            self.role = "reader"

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Values setup during registration
    clientId = os.getenv('CLIENTID')
    clientSecret = os.getenv('CLIENTSECRET')
    loginDisabled = app.config.get('LOGIN_DISABLED')
    githubClient = WebApplicationClient(clientId)

    @app.route('/login/callback')
    def call_back():
        callbackCode = request.args.get("code")
        tokenUrl, headers, body = githubClient.prepare_token_request("https://github.com/login/oauth/access_token", code=callbackCode)
        headers["Accept"] = "application/json"
        r = requests.post(
            tokenUrl,
            headers=headers,
            data=body,
            auth=(clientId, clientSecret),
        )
        params=githubClient.parse_request_body_response(r.text)
        print(params['access_token'])
        tokenUrl, headers, body = githubClient.add_token("https://api.github.com/user")
        userInfo = requests.get(
            tokenUrl,
            headers=headers,
            data=body,
        )
        userInfo = userInfo.json()
        print((userInfo['login']))
        login_user(load_user(userInfo['login']))
        return redirect('/')

    @login_manager.unauthorized_handler 
    def unauthenticated():
        githubRedirect = githubClient.prepare_request_uri("https://github.com/login/oauth/authorize")
        print(githubRedirect)
        return redirect(githubRedirect)

    @login_manager.user_loader 
    def load_user(user_id):
        user = User(user_id)
        return user

    def validate_user_role(func):
        @wraps(func)
        def wrapTheFunction(*args, **kwargs):
            if loginDisabled:
                if (current_user.role == "reader"):
                    return render_template("error.html", error="Insufficient User Rights")
                return func(*args, **kwargs)
            return func(*args, **kwargs)    
        return wrapTheFunction

    @app.route('/')
    @login_required
    def get_items():
        return render_template("index.html", model=ViewModel(MongoActions().get_cards()))

    @app.route('/add_item', methods=['POST'])
    @login_required
    @validate_user_role
    def add_new_item():
        title = request.form['title']
        MongoActions().add_new_card(title)
        return redirect('/')

    @app.route('/move_item/<id>', methods=['POST'])
    @login_required
    @validate_user_role
    def move_item(id):
        MongoActions().update_card_status(id)
        return redirect('/')
    
    @app.route('/delete_item/<id>', methods=['POST'])
    @login_required
    @validate_user_role
    def delete_item(id):
        MongoActions().delete_card(id)
        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

from flask import Flask, render_template, request, redirect
import todo_app.data.session_items
import os

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def get_items():
    items = todo_app.data.session_items.get_items()
    return render_template("index.html", items=items)

@app.route('/add_item', methods=['POST', 'GET'])
def add_new_item():
    title = request.form['title']
    if request.method == 'POST':
        title = request.form.get("title")
        todo_app.data.session_items.add_item(title)
        return redirect(os.getenv("HOSTNAME_GITPOD"))
    # todo_app.data.session_items.add_item(title)
    # return redirect(f"/")
    # todo_app.data.session_items.add_item(title)
    # items = todo_app.data.session_items.get_items()
    # return render_template("index.html", items=items)
    # return redirect("/")

if __name__ == '__main__':
    app.run()

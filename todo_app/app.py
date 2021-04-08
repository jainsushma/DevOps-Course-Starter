from flask import Flask, render_template, request
import todo_app.data.session_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/items')
def get_items():
    items = todo_app.data.session_items.get_items()
    return render_template("index.html", items=items)

@app.route('/item', methods=['POST'])
def add_item():
    title = request.form['title']
    todo_app.data.session_items.add_item(title)
    items = todo_app.data.session_items.get_items()
    return render_template("index.html", items=items)

if __name__ == '__main__':
    app.run()

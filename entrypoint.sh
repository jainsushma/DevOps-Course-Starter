#Setting port environment variable
poetry run gunicorn --bind 0.0.0.0:${PORT:-5000} "todo_app.app:create_app()"
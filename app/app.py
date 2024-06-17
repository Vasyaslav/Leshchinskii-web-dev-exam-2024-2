from flask import Flask, render_template, request, send_from_directory
from flask_login import current_user
from mysqldb import DBConnector
import mysql.connector as connector

app = Flask(__name__)
application = app
app.config.from_pyfile("config.py")

db_connector = DBConnector(app)
from auto import bp as auto_bp, init_login_manager

app.register_blueprint(auto_bp)
init_login_manager(app)

from users import bp as users_bp

app.register_blueprint(users_bp)

from books import bp as books_bp

app.register_blueprint(books_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/images/<image_id>')
def image(image_id):
    # Получение иллюстрации к товару
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute(
            "SELECT * FROM images WHERE id = %s", [image_id]
        )
        print(cursor.statement)
        img = cursor.fetchone()
    print(img)
    print(app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.file_name)


# python -m venv ve
# . ve/bin/activate -- Linux
# ve\Scripts\activate -- Windows
# pip install flask python-dotenv
# cd app
# flask run

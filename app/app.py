from flask import Flask, render_template, request, send_from_directory
from flask_login import current_user
from mysqldb import DBConnector
import mysql.connector as connector
from math import ceil

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


from reviews import bp as reviews_bp

app.register_blueprint(reviews_bp)


MAX_PER_PAGE = 5


@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    books_data = {}
    with db_connector.connect().cursor(named_tuple=True, buffered=True) as cursor:
        query = ('select * from books ORDER BY year '
                 f'LIMIT {MAX_PER_PAGE} OFFSET {(page - 1) * MAX_PER_PAGE}')
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        for book_data in data:
            books_data[book_data.name] = {"id": book_data.id, "year": book_data.year, "genres": []}
            query = ('SELECT genre FROM book_genre join '
                     'genres on book_genre.genre_id = genres.id WHERE '
                     'book_id = %s')
            cursor.execute(query, (book_data.id,))
            for genre in cursor.fetchall():
                books_data[book_data.name]["genres"].append(genre.genre)
        for book in books_data:
            cursor.execute('SELECT COUNT(*) as "count", AVG(rating) as "avg" FROM reviews WHERE '
                           'book_id = %s group by book_id', (books_data[book]["id"],))
            reviews_data = cursor.fetchone()
            books_data[book]["reviews_data"] = reviews_data
        cursor.execute("SELECT COUNT(*) as count FROM books")
        record_count = cursor.fetchone().count
        page_count = ceil(record_count / MAX_PER_PAGE)
        pages = range(max(1, page - 3), min(page_count, page + 3) + 1)
        print(record_count)
    return render_template("index.html", books_data=books_data, page=page, page_count=page_count, pages=pages)


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

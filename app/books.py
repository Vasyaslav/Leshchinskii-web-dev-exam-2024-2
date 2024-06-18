from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
import hashlib
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from auto import check_rights
from app import db_connector
import mysql.connector as connector
from werkzeug.utils import secure_filename
from os.path import join
from os import remove
from bleach import clean

bp = Blueprint("books", __name__, url_prefix="/books")

ratings = {5: "Отлично", 4: "Хорошо", 3: "Удовлетворительно",
           2: "Неудовлетворительно", 1: "Плохо", 0: "Ужасно"}

@bp.route("<int:book_id>/view")
def view(book_id):
    connection = db_connector.connect()
    current_user_review = ''
    reviews = ''
    with connection.cursor(named_tuple=True, buffered=True) as cursor:
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        print("book =", book)
        cursor.execute("SELECT * FROM images WHERE id = %s", (book.image_id,))
        image = cursor.fetchone()
        print("image =", image)
        query = ("SELECT genre FROM book_genre JOIN "
                 "genres on genre_id = id WHERE book_id = %s")
        cursor.execute(query, (book_id,))
        genres = cursor.fetchall()
        print("genres =", genres)
        if current_user.is_authenticated:
            query = ("SELECT rating, text, users.* FROM reviews JOIN "
                     "users on reviews.user_id = users.id WHERE "
                     "book_id = %s and user_id != %s")
            cursor.execute(query, (book_id, current_user.id))
            reviews = cursor.fetchall()
            print("reviews =", reviews)
            cursor.execute("SELECT * FROM reviews WHERE book_id = %s and user_id = %s", (book_id, current_user.id))
            current_user_review = cursor.fetchone()
            print("current_user_review =", current_user_review)
        else:
            query = ("SELECT rating, text, users.* FROM reviews JOIN "
                     "users on reviews.user_id = users.id WHERE "
                     "book_id = %s")
            cursor.execute(query, (book_id,))
            reviews = cursor.fetchall()
    return render_template("books/view.html", book=book, image=image, reviews=reviews,
     genres=genres, current_user_review=current_user_review, ratings=ratings)


@bp.route("/new", methods = ["GET", "POST"])
@login_required
@check_rights("create")
def new():
    connection = db_connector.connect()
    with connection.cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT * FROM genres")
        genres = cursor.fetchall()
    if request.method == "POST":
        try:
            connection = db_connector.connect()
            with connection.cursor(named_tuple=True, buffered=True) as cursor:
                if "book_img" in request.files and secure_filename(request.files["book_img"].filename):
                    book_img = request.files["book_img"]
                    image_bytes = book_img.read()
                    image_hash = hashlib.md5(image_bytes).hexdigest()
                    print(secure_filename(book_img.filename), book_img.mimetype, image_hash)
                    cursor.execute("SELECT * from images WHERE md5_hash = %s", (image_hash,))
                    print(1)
                    is_image = cursor.fetchone()
                    if is_image:
                        image_id = is_image.id
                    else:
                        image_data = [image_hash + "." + secure_filename(book_img.filename).split(".")[-1], book_img.mimetype, image_hash]
                        query = ('INSERT INTO images (file_name, mime_type, md5_hash) '
                                 'VALUES(%s, %s, %s)')
                        print(2)
                        cursor.execute(query, image_data)
                        image_id = cursor.lastrowid
                        print(image_id)
                        with open(join(current_app.config["UPLOAD_FOLDER"], image_data[2] + "." + image_data[0].split(".")[-1]), "wb") as image_to_save:
                            image_to_save.write(image_bytes)
                        print(cursor.statement)

                fields = ["book_name", "book_author", "book_publisher", "book_year", "book_volume", "book_description"]
                book_data = {field: request.form[field].strip().capitalize() for field in fields}
                book_data["book_description"] = clean(book_data["book_description"])
                book_data["image_id"] = image_id
                query = ('INSERT INTO books(name, description, year, publisher, author, volume, image_id) '
                         'VALUES(%(book_name)s, %(book_description)s, %(book_year)s, %(book_publisher)s, '
                         '%(book_author)s, %(book_volume)s, %(image_id)s)')
                cursor.execute(query, book_data)
                print(cursor.statement)
                book_id = cursor.lastrowid
                for genre in request.form.getlist("book_genre"):
                    cursor.execute('INSERT INTO book_genre VALUES(%s, %s)', (book_id, genre))
                connection.commit()
            return redirect(url_for("books.view", book_id = book_id))
        except connector.errors.DatabaseError as e:
            flash(
                f"Произошла ошибка при добавлении данных о книге. Нарушение связи с базой данных. {e}",
                "danger",
            )
            connection.rollback()
    return render_template("books/new.html", genres=genres)


@bp.route("<int:book_id>/edit", methods = ["GET", "POST"])
@login_required
@check_rights("update_book")
def edit(book_id):
    connection = db_connector.connect()
    with connection.cursor(named_tuple=True, buffered=True) as cursor:
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book_data = cursor.fetchone()
        cursor.execute("SELECT * FROM genres")
        genres = cursor.fetchall()
        cursor.execute("SELECT id, genre FROM book_genre JOIN genres on genre_id = id WHERE book_id = %s", (book_id,))
        book_genres = cursor.fetchall()
        book_genres_id = []
        for genre in book_genres:
            book_genres_id.append(genre.id)
        print(book_genres_id)
    if request.method == "POST":
        try:
            connection = db_connector.connect()
            with connection.cursor(named_tuple=True, buffered=True) as cursor:
                fields = ["book_name", "book_author", "book_publisher", "book_year", "book_volume", "book_description"]
                book_data = {field: request.form[field].strip().capitalize() for field in fields}
                book_data["id"] = book_id
                book_data["book_description"] = clean(book_data["book_description"])
                query = ('UPDATE books SET '
                         'name = %(book_name)s, description = %(book_description)s, '
                         'year = %(book_year)s, publisher = %(book_publisher)s, '
                         'author = %(book_author)s, volume = %(book_volume)s WHERE '
                         'id = %(id)s')
                cursor.execute(query, book_data)
                print(cursor.statement)
                cursor.execute("DELETE FROM book_genre WHERE book_id = %s", (book_id,))
                print(12222222)
                print(book_id, request.form.getlist("book_genre"))
                connection.commit()
                for genre in request.form.getlist("book_genre"):
                    cursor.execute('INSERT INTO book_genre VALUES(%s, %s)', (book_id, genre))
                connection.commit()
            return redirect(url_for("books.view", book_id = book_id))
        except connector.errors.DatabaseError as e:
            flash(
                f"Произошла ошибка при изменении данных о книге. Нарушение связи с базой данных. {e}",
                "danger",
            )
            connection.rollback()
    return render_template("books/edit.html", genres=genres, book_data=book_data, book_genres_id=book_genres_id)


@bp.route("/<int:book_id>/delete", methods=["POST"])
@login_required
@check_rights("delete_book")
def delete(book_id):
    # Удаление книги
    try:
        connection = db_connector.connect()
        with connection.cursor(named_tuple=True, buffered=True) as cursor:
            cursor.execute("SELECT image_id FROM books WHERE id = %s", (book_id,))
            image_id = cursor.fetchone()
            print(image_id)
            query = "DELETE FROM books WHERE id = %s"
            cursor.execute(query, (book_id,))
            connection.commit()
            cursor.execute("SELECT * FROM books WHERE image_id = %s", (image_id.image_id,))
            if not cursor.fetchall():
                cursor.execute("SELECT * FROM images WHERE id = %s", (image_id.image_id,))
                file_name = cursor.fetchone()
                remove(join(current_app.config["UPLOAD_FOLDER"], file_name.file_name))
                cursor.execute("DELETE FROM images WHERE id = %s", (image_id.image_id,))
                connection.commit()
        flash("Книга успешно удалена", "success")
    except connector.errors.DatabaseError as e:
        flash(
            f"Произошла ошибка при изменении удалении о книги. Нарушение связи с базой данных. {e}",
            "danger",
        )
        connection.rollback()
    return redirect(url_for("index"))

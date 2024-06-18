from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
import hashlib
from flask_login import login_required
from auto import check_rights
from app import db_connector
import mysql.connector as connector
from bleach import clean

bp = Blueprint("reviews", __name__, url_prefix="/reviews")

ratings = {5: "Отлично", 4: "Хорошо", 3: "Удовлетворительно",
           2: "Неудовлетворительно", 1: "Плохо", 0: "Ужасно"}

@bp.route("/<int:book_id>/<int:user_id>/new_review", methods=["GET", "POST"])
@login_required
def new(book_id, user_id):
    # Добавление рецензии
    if request.method == "POST":
        try:
            connection = db_connector.connect()
            with connection.cursor(named_tuple=True, buffered=True) as cursor:
                query = ('INSERT INTO reviews(book_id, user_id, rating, text) '
                         'VALUES(%s, %s, %s, %s)')
                cursor.execute(query, (book_id, user_id, request.form["review_rating"], 
                clean(request.form["review_text"]).strip().capitalize()))
                connection.commit()
            flash("Рецензия успешно добавлена", "success")
            return redirect(url_for("books.view", book_id=book_id))
        except connector.errors.DatabaseError as e:
            flash(
                f"Произошла ошибка при добавлении рецензии. Нарушение связи с базой данных. {e}",
                "danger",
            )
            connection.rollback()
    return render_template("reviews/new.html", ratings=ratings)


@bp.route("/<int:book_id>/<int:user_id>/edit_review", methods=["GET", "POST"])
@login_required
def edit(book_id, user_id):
    # Редактирование рецензии
    with db_connector.connect().cursor(named_tuple=True, buffered=True) as cursor:
        cursor.execute("SELECT * FROM reviews WHERE user_id = %s and book_id = %s", (user_id, book_id))
        review_data = cursor.fetchone()
    if request.method == "POST":
        try:
            print(2)
            connection = db_connector.connect()
            with connection.cursor(named_tuple=True, buffered=True) as cursor:
                print(1)
                query = ('UPDATE reviews SET '
                         'rating = %s, text = %s WHERE '
                         'user_id = %s and book_id = %s')
                cursor.execute(query, (request.form["review_rating"], 
                clean(request.form["review_text"]).strip().capitalize(), user_id, book_id))
                print(cursor.statement)
                connection.commit()
                cursor.execute("SELECT * FROM reviews WHERE user_id = %s and book_id = %s", (user_id, book_id))
                print(cursor.fetchone())
            flash("Рецензия успешно изменена", "success")
            return redirect(url_for("books.view", book_id=book_id))
        except connector.errors.DatabaseError as e:
            flash(
                f"Произошла ошибка при изменении рецензии. Нарушение связи с базой данных. {e}",
                "danger",
            )
            connection.rollback()
    print(review_data)
    return render_template("reviews/edit.html", ratings=ratings, review_data=review_data)
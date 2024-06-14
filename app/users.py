from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db_connector
from flask_login import login_required, current_user
from auto import check_rights
import mysql.connector as connector
from werkzeug.utils import secure_filename
import csv
from os.path import join
from os import remove

bp = Blueprint("users", __name__, url_prefix="/users")


def get_roles():
    result = []
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT * FROM roles")
        result = cursor.fetchall()
    return result


@bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
@check_rights("delete_user")
def delete_user(user_id):
    # Удаление пользователя
    connection = db_connector.connect()
    with connection.cursor(named_tuple=True) as cursor:
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
    flash("Учетная запись успешно удалена", "success")
    return redirect(url_for("index"))


@bp.route("/reg", methods=["POST", "GET"])
def reg():
    # Регистрация пользователя
    user_data = {}
    if request.method == "POST":
        fields = (
            "login",
            "password",
            "first_name",
            "middle_name",
            "last_name",
        )
        user_data = {field: request.form[field] or None for field in fields}
        try:
            connection = db_connector.connect()
            with connection.cursor(named_tuple=True) as cursor:
                query = (
                    "INSERT INTO users (login, password_hash, first_name, middle_name, last_name, role_id) VALUES "
                    "(%(login)s, SHA2(%(password)s, 256), %(first_name)s, %(middle_name)s, %(last_name)s, 1)"
                )
                cursor.execute(query, user_data)
                print(cursor.statement)
                connection.commit()
            flash("Учетная запись успешно создана", "success")
            return redirect(url_for("users.index"))
        except connector.errors.DatabaseError:
            flash(
                "Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены",
                "danger",
            )
            connection.rollback()
    return render_template("users/reg.html", user_data=user_data, roles=get_roles())

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from functools import wraps
from app import db_connector
from users_policy import UsersPolicy

bp = Blueprint("auto", __name__, url_prefix="/auto")


def init_login_manager(app):
    # Подключение к приложению модуля для авторизации пользователей
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auto.auth"
    login_manager.login_message = "Авторизуйтесь для доступа к этому ресурсу"
    login_manager.login_message_category = "warning"
    login_manager.user_loader(load_user)


class User(UserMixin):
    # Класс для пользователей
    def __init__(self, user_id, user_login, role_id):
        self.id = user_id
        self.user_login = user_login
        self.role_id = role_id

    def is_moderator(self):
        return self.role_id == current_app.config["MODER_ROLE_ID"]

    def is_admin(self):
        return self.role_id == current_app.config["ADMIN_ROLE_ID"]

    def can(self, action, user=None):
        policy = UsersPolicy(user)
        return getattr(policy, action, lambda: False)()


def load_user(user_id):
    # Авторизатор пользователей
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute(
            "SELECT id, login, role_id FROM users WHERE id = %s;", (user_id,)
        )
        user = cursor.fetchone()
    if user is not None:
        return User(user.id, user.login, user.role_id)
    return None


def check_rights(action):
    # Декоратор для проверки прав доступа текущего пользователя
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = None
            print(1111)
            if "user_id" in kwargs.keys():
                with db_connector.connect().cursor(named_tuple=True) as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE id = %s;", (kwargs.get("user_id"),)
                    )
                    user = cursor.fetchone()
            if not current_user.can(action, user):
                print(action, current_user.id)
                flash("Недостаточно прав для доступа к этой странице", "warning")
                return redirect(url_for("index"))
            return function(*args, **kwargs)

        return wrapper

    return decorator


@bp.route("/auth", methods=["POST", "GET"])
def auth():
    # Авторизация пользователя
    error = ""
    if request.method == "POST":
        login = request.form["username"]
        password = request.form["password"]
        remember_me = request.form.get("remember_me", None) == "on"
        with db_connector.connect().cursor(named_tuple=True, buffered=True) as cursor:
            print(login)
            cursor.execute(
                "SELECT id, login, role_id FROM users WHERE login = %s AND pass_hash = SHA2(%s, 256)",
                (login, password),
            )
            print(cursor.statement)
            user = cursor.fetchone()

        if user is not None:
            flash("Авторизация прошла успешно", "success")
            login_user(User(user.id, user.login, user.role_id), remember=remember_me)
            next_url = request.args.get("next", url_for("index"))
            return redirect(next_url)
        flash("Невозможно аутентифицироваться с указанными логином и паролем", "danger")
    return render_template("auth.html")


@bp.route("/logout")
def logout():
    # Деавторизация пользователя
    print(current_user)
    logout_user()
    return redirect(url_for("index"))

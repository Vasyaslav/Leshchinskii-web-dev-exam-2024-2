from flask_login import current_user


class UsersPolicy:
    # Класс для проверки выполнимости пользователем каких-либо действий
    def __init__(self, user):
        self.user = user

    def create(self):
        return current_user.is_admin()

    def add_review(self):
        return current_user.is_authenticated
    
    def update_review(self):
        return current_user.is_admin() or current_user.is_moderator() or current_user.id == self.user.id

    def delete_user(self):
        return current_user.is_admin() or current_user.id == self.user.id
    
    def update_book(self):
        return current_user.is_admin() or current_user.is_moderator()

    def delete_book(self):
        return current_user.is_admin()

    def assign_role(self):
        return current_user.is_admin()

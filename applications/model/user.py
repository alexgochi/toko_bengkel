from flask_login import UserMixin
# Define User class
class User(UserMixin):
    def _init_(self, id, name, level):
        self.id = id
        self.name = name
        self.level = level

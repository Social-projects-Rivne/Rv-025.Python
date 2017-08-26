"""
Contain a model class for users.
"""

from client_app import db, bcrypt


class User(db.Model):

    """Implement a fully featured User model and handle users data in DB."""

    __tablename__ = 'users'

    STATUS_ACTIVE = 0
    STATUS_DELETED = 1
    STATUS_BANNED = 2
    STATUS_UNAUTHORIZED = 3

    ROLE_USER = 3

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(12), unique=True)
    avatar = db.Column(db.String(512), nullable=True)
    role = db.Column(db.Integer, default=ROLE_USER, nullable=False)
    status = db.Column(db.Integer, default=STATUS_ACTIVE, nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    parent = db.relationship('User', foreign_keys=parent_id)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        return " ".join(self.name, self.email)

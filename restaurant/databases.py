from restaurant import db, login_Manager
from flask_login import UserMixin

@login_Manager.user_loader
def loadUser(userID) : 
    return User.query.get(int(userID))

class User(db.Model, UserMixin) :
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    email = db.Column(db.String(125), unique = True, nullable = False)
    image_icon = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    points = db.Column(db.Integer, default = 0)
    orders = db.relationship('Order', backref = 'customer', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Order(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    orderName = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable = False)
    price = db.Column(db.String(50), nullable = False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    complete = db.Column(db.Boolean, default = False, nullable = False)

    def __repr__(self) :
        return f"Order('{self.orderName}')"

class Menu(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    orderName = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable = False)
    price = db.Column(db.String(50), nullable = False)
    section = db.Column(db.Integer, nullable = False)

    def __repr__(self) :
        return f"Order('{self.orderName}')"
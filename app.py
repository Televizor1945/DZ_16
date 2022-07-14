import json
import data
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# from models import User, Order, Offer
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


db.drop_all()
db.create_all()

for user in data.USER:
    db.session.add(User(
        id=user["id"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    ))

for order in data.ORDERS:
    month_start, day_start, year_start = [int(o) for o in order['start_date'].split("/")]
    month_end, day_end, year_end = order['end_date'].split("/")

    db.session.add(Order(
        id=order["id"],
        name=order["name"],
        description=order["description"],
        start_date=datetime.date(year=year_start, month=month_start, day=day_start),
        end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=order["address"],
        price=order["price"],
        customer_id=order["customer_id"],
        executor_id=order["executor_id"]
    ))

db.session.add_all([Offer(id=offer["id"], order_id=offer["order_id"], executor_id=offer["executor_id"]) for offer in data.OFFERS])

db.session.commit()

@app.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        user_data = User.query.all()

        user_response = []
        for user in user_data:
            user_response.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "email": user.email,
                    "role": user.role,
                    "phone": user.phone
                }
            )


        return json.dumps([user.to_dict() for user in user_data]), 200

    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            new_user_obj = User(
                id=user["id"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                age=user["age"],
                email=user["email"],
                role=user["role"],
                phone=user["phone"]
            )
            db.session.add(new_user_obj)
            db.session.commit()
            db.session.close()
            return "Пользователь создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/users/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Не найдено"
        else:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = User.query.all()
        user = User.query.get(user_id)
        if user is None:
            return "Пользователь не найден!", 404
        user.first_name = user_data["first_name"],
        user.last_name = user_data["last_name"],
        user.age = user_data["age"],
        user.email = user_data["email"],
        user.role = user_data["role"],
        user.phone = user_data["phone"]
        db.session.add(user)
        db.session.commit()

        return f"Объект с id {user_id} успешно изменён!", 200
    elif request.method == 'DELETE':
        user = User.query.get(user_id)
        if user is None:
            return "Пользователь не найден!", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Объект с id {user_id} успешно удалён!", 200


@app.route('/orders/', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        order_data = Order.query.all()
        return jsonify([order.to_dict() for order in order_data]), 200
    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(o) for o in order['start_date'].split("/")]
            month_end, day_end, year_end = order['end_date'].split("/")
            new_order_obj = Order(
                id=order["id"],
                name=order["name"],
                description=order["description"],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
                address=order["address"],
                price=order["price"],
                customer_id=order["customer_id"],
                executor_id=order["executor_id"]
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return "Заказ создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>/', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Не найдено"
        else:
            return jsonify(order.to_dict())


@app.route('/offers/', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        offer_data = Offer.query.all()
        return jsonify([offer.to_dict() for offer in offer_data]), 200
    if request.method == 'POST':
        try:
            offer = json.loads(request.data)
            new_offer_obj = Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
            db.session.add(new_offer_obj)
            db.session.commit()
            db.session.close()
            return "Предложение создано в базе данных", 200
        except Exception as e:
            return e


@app.route('/offers/<int:offer_id>/', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Не найдено"
        else:
            return jsonify(offer.to_dict())


if __name__ == '__main__':
    app.run(debug=True)

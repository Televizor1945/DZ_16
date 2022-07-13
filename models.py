# from app import db
# import datetime
# import data
#

# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     age = db.Column(db.Integer)
#     email = db.Column(db.String(100))
#     role = db.Column(db.String(100))
#     phone = db.Column(db.String(100))
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "age": self.age,
#             "email": self.email,
#             "role": self.role,
#             "phone": self.phone
#         }
#
# class Order(db.Model):
#     __tablename__ = "order"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     description = db.Column(db.Text)
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
#     address = db.Column(db.String(100))
#     price = db.Column(db.Float)
#     customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "description": self.description,
#             "start_date": self.start_date,
#             "end_date": self.end_date,
#             "address": self.address,
#             "price": self.price,
#             "customer_id": self.customer_id,
#             "executor_id": self.executor_id
#         }
#
# class Offer(db.Model):
#     __tablename__ = "offer"
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "order_id": self.order_id,
#             "executor_id": self.executor_id
#         }
#
# db.drop_all()
# db.create_all()
#
# for user in data.USER:
#     db.session.add(User(
#         id=user["id"],
#         first_name=user["first_name"],
#         last_name=user["last_name"],
#         age=user["age"],
#         email=user["email"],
#         role=user["role"],
#         phone=user["phone"]
#     ))
#
#
# for order in data.ORDERS:
#     month_start, day_start, year_start = [int(o) for o in order['start_date'].split("/")]
#     month_end, day_end, year_end = order['end_date'].split("/")
#
#     db.session.add(Order(
#         id=order["id"],
#         name=order["name"],
#         description=order["description"],
#         start_date=datetime.date(year=year_start, month=month_start, day=day_start),
#         end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
#         address=order["address"],
#         price=order["price"],
#         customer_id=order["customer_id"],
#         executor_id=order["executor_id"]
#     ))
#
# db.session.add_all([Offer(id=offer["id"], order_id=offer["order_id"], executor_id=offer["executor_id"]) for offer in data.OFFERS])
#
# db.session.commit()


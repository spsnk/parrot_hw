
import decimal
from uuid import uuid4

from api.models.product import Products
from api.models.shared import ModelToDict, db
from api.models.user import Users
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.types import DateTime, Integer, Numeric, String


class Orders(db.Model, ModelToDict):
    id: str = Column(String, primary_key=True, default=func.gen_random_uuid())
    user_email: str = Column(String, ForeignKey(
        column=Users.email))
    total: decimal.Decimal = Column(Numeric(10, 2))
    date_created = Column(DateTime(timezone=True),
                          server_default=func.current_timestamp(), index=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<{self.id}>{self.user_email} [{self.date_created}]: ${self.total.__float__()}'


class OrderContents(db.Model, ModelToDict):
    __tablename__ = "ordercontents"
    order_id: str = Column(String, ForeignKey(
        column=Orders.id), primary_key=True)
    product_id: str = Column(String, ForeignKey(
        column=Products.id), primary_key=True)
    unitary_price: decimal.Decimal = Column(
        Numeric(10, 2, asdecimal=True), index=True)
    quantity: int = Column(Integer)

    def __repr__(self):
        return f'Order <{self.order_id}> {Products.query.get(self.product_id).name} (${self.unitary_price.__float__()}) x {self.quantity}'

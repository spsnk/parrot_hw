import decimal
from uuid import uuid4

from api.models.shared import ModelToDict, db
from sqlalchemy import Column
from sqlalchemy.types import Numeric, String


class Products(db.Model, ModelToDict):
    id: str = Column(String, primary_key=True, default=uuid4().__str__())
    name: str = Column(String, unique=True, index=True)
    unitary_price: decimal.Decimal = Column(Numeric(10, 2))

    def create(self):
        self.name = self.name.strip().lower()
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'{self.name}: ${self.unitary_price}'

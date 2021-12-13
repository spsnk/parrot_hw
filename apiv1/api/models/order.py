import datetime
import decimal
from uuid import uuid4

from api.models.shared import ModelToDict, db
from api.models.user import Users
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Date, Numeric, String


class Order(db.Model, ModelToDict):
    id: str = Column(String, primary_key=True, default=uuid4().__str__())
    user_email: str = Column(String, ForeignKey(column=Users.email))
    # add onupdate to update total
    total: decimal.Decimal = Column(Numeric(10, 2))
    date_created = Column(Date, server_default=func.current_date(), index=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'{self.user_email} [{datetime.datetime.fromtimestamp(self.date_created)}]: ${self.total}'

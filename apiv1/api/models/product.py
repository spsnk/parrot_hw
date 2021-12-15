import decimal
from uuid import uuid4

from api.models.shared import ModelToDict, db
from sqlalchemy import Column, func
from sqlalchemy.types import Numeric, String


class Products(db.Model, ModelToDict):
    id: str = Column(String, primary_key=True, default=func.gen_random_uuid())
    name: str = Column(String, unique=True, index=True)

    def create(self):
        self.name = self.name.strip().lower()
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'{self.id} [{self.name}]'

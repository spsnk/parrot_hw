from api.models.shared import ModelToDict, db

from sqlalchemy import Column
from sqlalchemy.types import String


class Users(db.Model, ModelToDict):
    email: str = Column(String, primary_key=True)
    name: str = Column(String)

    def create(self):
        self.email = self.email.strip().lower()
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'{self.name} <{self.email}>'

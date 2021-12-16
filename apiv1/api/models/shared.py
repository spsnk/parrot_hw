from api.common.util import convert_decimal
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


class ModelToDict():

    def get_dict(self):
        return {col.name: convert_decimal(getattr(self, col.name)) for col in self.__table__.columns}

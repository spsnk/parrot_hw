from flask_sqlalchemy import SQLAlchemy

from api.common.util import convert_decimal

db: SQLAlchemy = SQLAlchemy()


class ModelToDict():

    def get_dict(self):
        return {col.name: convert_decimal(getattr(self, col.name)) for col in self.__table__.columns}

from api.models.shared import db


class Users(db.Model):
    email = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.get_dict()

    def get_dict(self):
        return {
            "email": self.email,
            "name": self.name
        }

    def __repr__(self):
        return f'{self.name} <{self.email}>'

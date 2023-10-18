from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY


class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    year =  db.Column(db.Integer, nullable = False)
    title = db.Column(db.String, unique = True, nullable = False)
    studios =  db.Column(db.String, nullable = False)
    producers = db.Column(db.String, nullable = False)
    winner = db.Column(db.String, nullable = True)

    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'title': self.title,
            'studios':self.studios,
            'producers':self.producers,
            'winner': self.winner if self.winner else ''
        }
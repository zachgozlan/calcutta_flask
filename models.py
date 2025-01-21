from flask_app import db

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=False))
    name = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=False)
    team = db.Column(db.String(30), index=False, unique=False)
    bid = db.Column(db.Numeric(10,2))

    def __repr__(self):
        return '<Bid {}>'.format(self.id)

def __init__(self, id, timestamp, name, email, team, bid):
   self.id = id
   self.timestamp = timestamp
   self.name = name
   self.team = team
   self.bid = bid
from database.database import db

class Record(db.Model):
    __tablename__ = 'records' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user = db.Column(db.String(150), nullable = False)
    time = db.Column(db.String(150), nullable = False)
    description = db.Column(db.String(255), nullable = False)

    def __init__(self, user, time, description):
        self.user = user
        self.time = time
        self.description = description

    def __repr__(self):
        return '<Record %r>' % self.id

    @staticmethod
    def get_records():
        return Record.query.all()
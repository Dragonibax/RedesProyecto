from database.database import db

class SSHUser(db.Model):
    __tablename__ = 'sshusers'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    router_id = db.Column(db.Integer, nullable = False)

    def __init__(self, username, password, router_id):
        self.username = username
        self.password = password
        self.router_id = router_id

    def __repr__(self):
        return '<SSHUser %r>' % self.id

    def update_username(self,username):
        self.username = username
        db.session.commit()

    def update_password(self,password):
        self.password = password
        db.session.commit()

    @staticmethod
    def get_by_router(id):
        return SSHUser.query.filter_by(router_id=id).all()

    @staticmethod
    def get_by_id(id):
        return SSHUser.query.filter_by(id=id).first()

    @staticmethod
    def get_by_username(username):
        return SSHUser.query.filter_by(username=username).first()
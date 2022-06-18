from database.database import db

class IfData(db.Model):
    __tablename__ = 'ifdata'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    interface = db.Column(db.String(100), unique = False)
    inpackets = db.Column(db.Integer, nullable = False)
    inerrors = db.Column(db.Integer, nullable = False)
    outpackets = db.Column(db.Integer, nullable = False)
    ifstatus = db.Column(db.Integer, nullable = False)
    time = db.Column(db.String(30), nullable = False)

    def __init__(self, interface, inpackets, inerrors, outpackets, ifstatus, time):
        self.interface = interface
        self.inpackets = inpackets
        self.inerrors = inerrors
        self.outpackets = outpackets
        self.ifstatus = ifstatus
        self.time = time 

    def __repr__(self):
        return '<IfData %r>' % self.id

    @staticmethod
    def get_data(interface):
        return IfData.query.filter_by(interface = interface).all()

    @staticmethod
    def get_last_record(interface):
        return IfData.query.filter_by(interface=interface).order_by(IfData.id.desc()).first()

    @staticmethod
    def delete_all():
        IfData.query.delete()
        db.session.commit()

class Interface(db.Model):
    __tablename__ = 'interface'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    interface = db.Column(db.String(100), unique = False)
    
    def __init__(self, interface):
        self.interface = interface
        
    def __repr__(self):
        return '<Interface %r>' % self.id

    @staticmethod
    def get_interfaces():
        return Interface.query.all()

    @staticmethod     
    def reset_interfaces():
        Interface.query.delete()
        db.session.commit()
from database import db

class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(100), nullable=False)

    package = db.Column(db.String(50), nullable=False)

    location = db.Column(db.String(100))

    eligible_department = db.Column(db.String(200))

    minimum_cgpa = db.Column(db.Float)

    last_date = db.Column(db.String(30))

    logo = db.Column(db.String(255), nullable=True)

    is_active = db.Column(db.Boolean, default=True)

    
    
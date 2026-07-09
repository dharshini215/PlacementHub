from database import db


class Student(db.Model):

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    register_number = db.Column(db.String(30), unique=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    phone = db.Column(db.String(15))

    department = db.Column(db.String(50))

    year = db.Column(db.String(10))

    cgpa = db.Column(db.Float)

    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Student {self.full_name}>"
    
    resume = db.Column(db.String(255), nullable=True)
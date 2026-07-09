from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Notification(db.Model):

    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    message = db.Column(
        db.String(300),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
)
    
    


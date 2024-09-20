from config import app, db
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    about_text = db.Column(db.String(300), unique=False, nullable=False)
    img = db.Column(db.String, unique=False, nullable=False)
    blog_url = db.Column(db.String, unique=False, nullable=False)

    
    def to_json(self):

        just_date = self.date.strftime("%b %d, %Y") if self.date else None
        return {
            "id": self.id,
            "title": self.title,
            "date": just_date,
            "aboutText": self.about_text,
            "img": self.img,
            "blogUrl": self.blog_url
        }


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    job_title = db.Column(db.String(60), unique=False, nullable=False)
    bio = db.Column(db.String, unique=False, nullable=False)
    img = db.Column(db.String, unique=False, nullable=False)
    public_id = db.Column(db.String, unique=False, nullable=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "jobTitle": self.job_title,
            "bio": self.bio,
            "img": self.img,
            "publicId": self.public_id
        }

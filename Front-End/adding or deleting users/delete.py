from app import db
from app.models import User

users = User.query.all()

for u in users:
	db.session.delete(u)
	db.session.commit()
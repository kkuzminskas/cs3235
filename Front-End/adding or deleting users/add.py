from app import db
from app.models import User

u = User(username='alice')
u.set_password('12345')
db.session.add(u)
db.session.commit()

u = User(username='bob')
u.set_password('53213')
db.session.add(u)
db.session.commit()

u = User(username='charlie')
u.set_password('67890')
db.session.add(u)
db.session.commit()

users = User.query.all()

for u in users:
	print(u.username, u.password, u.password_hash)
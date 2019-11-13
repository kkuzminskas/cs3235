from app import db
from app.models import User

# u = User(username='youkuan')
# u.set_password('12345')
# db.session.add(u)
# db.session.commit()

# u = User(username='siqi')
# u.set_password('1349')
# db.session.add(u)
# db.session.commit()

# u = User(username='ahmed')
# u.set_password('67890')
# db.session.add(u)
# db.session.commit()

# u = User(username='kendall')
# u.set_password('1359')
# db.session.add(u)
# db.session.commit()


users = User.query.all()

for u in users:
	# if u.username == 'siqi':
	# 	u.set_password('1946')
	# 	db.session.commit()
	print(u.username, u.password, u.password_hash)
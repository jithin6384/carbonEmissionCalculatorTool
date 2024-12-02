from app import User;


userList = User.query.all()
user = User.query.filter_by(email="johndoe@example.com").first()
# print(user.)
print(userList);
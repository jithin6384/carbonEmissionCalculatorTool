from app import User, db;


userList = User.query.all()

if not userList:
    print("no users in database");
else:
    for user in userList:
        db.session.delete(user);
        
    db.session.commit()
    print(f"deleted {len(userList)} from database")
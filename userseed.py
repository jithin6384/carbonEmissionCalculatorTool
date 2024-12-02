from app import User, db;


userList = [{"email": "johndoe@example.com",
             "username" : "JohnDoe",
             "company_name": "globalcorp", 
             "password" : "password",  },
             {"email": "janedoe@example.com",
             "username" : "janeDoe",
             "company_name": "energy tech", 
             "password" : "password",  },
             {"email": "michael@example.com",
             "username" : "Michaels",
             "company_name": "worldwrestling", 
             "password" : "password",  },
             {"email": "tripleh@example.com",
             "username" : "hunter",
             "company_name": "globalwrestlingentertaiment", 
             "password" : "password",  },
             {"email": "john12@example.com",
             "username" : "John12",
             "company_name": "globalcorp1", 
             "password" : "password",  },
             ]


for user_data in userList:
    try:
        user = User(email = user_data["email"],
                    username= user_data["username"],
                    company_name=user_data["company_name"],
                    password=user_data["password"])
        db.session.add(user);
    except Exception as error:
        print("an error occured ", error);



try:
 db.session.commit();
except Exception as error:
        print("an error occured ", error);

print(f"{len(userList)} users created successfully")
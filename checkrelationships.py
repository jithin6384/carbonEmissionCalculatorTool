from app import User, BuisnessTravel, Waste, EnergyUsage, db;

current_user = User.query.all()[0]
business_travell_all = BuisnessTravel.query.all();
print("current user",current_user.buisness_travel)
print(business_travell_all[0].user_id)
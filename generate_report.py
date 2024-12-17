import sys
import plotly.graph_objects as go
from app import  User 
from werkzeug.security import check_password_hash

# Function to verify user and fetch carbon footprint data
def generate_report():
    # Input email and password
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Fetch user from the database
    user = User.query.filter_by(email=email).first()

    if not user:
        print("No user found with this email.")
        sys.exit(1)

    
    if not check_password_hash(user.password_hash, password):
        print("Incorrect password. Access denied.")
        sys.exit(1)

    print(f"User verified: {user.username}, Company: {user.company_name}")

    
    energy_footprint = 0
    waste_footprint = 0
    travel_footprint = 0

    if user.energy_usage:
        energy_footprint = ((user.energy_usage.electricity_bill * 12 * 0.0005) + 
                           (user.energy_usage.natural_gas_bill * 12 * 0.0053) + 
                           (user.energy_usage.fuel_bill * 12 * 2.32));
    
    if user.waste:
        waste_footprint = (user.waste.waste_generated * 12) * (0.57 - (user.waste.recycling_percantage / 100))

    if user.buisness_travel:
        travel_footprint = (user.buisness_travel.kilometer_traveled / 1) * \
                           (user.buisness_travel.fuel_efficiency / 100) * 2.31

    
    categories = ['Energy Footprint', 'Waste Footprint', 'Travel Footprint']
    values = [energy_footprint, waste_footprint, travel_footprint]

    # using plottly to create the data
    fig = go.Figure(go.Bar(
        x=categories,
        y=values,
        text=[f"{v:.2f} kg CO2e" for v in values],
        textposition='auto',
        marker=dict(color=['green', 'blue', 'red'])
    ))

    fig.update_layout(
        title=f"Carbon Footprint Report for {user.company_name}",
        xaxis_title="Categories",
        yaxis_title="Carbon Footprint (kg CO2e)",
        template="plotly_white"
    )


    outputfile = f"{user.company_name}_carbon_report.html"
    fig.write_html(outputfile)
    print(f"check your report : {outputfile}")

if __name__ == "__main__":
    generate_report()

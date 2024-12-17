# carbonEmissionCalculatorTool

Overview
    Carbon Emission Calculator is a tool which is designed to help companies monitor their carbon footprint which includes
    1.Energy footprint which includes 1.1 Electricity Bill 1.2 Fuel Bill and 1.3 Natural gas Bill
    2.Waste footprint which includes 1.1 Waste Generated  and 1.2 Recycling Percantage
    3.Travel footprint which includes 1.1 Distance Travelled  and 1.2 Fuel Effiency of Vehicles

Features
    User Signup
    When User signups by Filling their Data which is (Email, Username, CompanyName, Password)
    User Login
    After registring they are redirected to Login page where they can enter their email and password
    Data Input
    After login the first time the user is redirected to welcome page where they can fill their data regrading the above parameters(Energy, Waste and Travel) after submiting their data they are redirected to Home page.
    Analytics and reporting 
    In home page the user can see the performance in the form of bar chart based on the data they have entered and calculations done in backend
    Suggestions are also given based on data they have entered Red indicates the maximum footprint Blue for second and Green for third.
    Download button for download the chart and suggestion
    Summary page where user can see the summary of the companies which are registered using this app and also they can compare trends based on 1.Total footprint 2. Energy Footprint 3. Waste Footprint 4. Travel Footprint


Tech Stack
    Backened
        Python 3.8
        Flask-python framework
        Flask-SqlAlchemy: For connecting to data based on ORM
        SQLLite: Database for local and deployed enviroment
        Flask-migrate for database migrations
    
    Frontend
        HTML5, CSS3, Bootstrap, Javascript
        Chart.js for visualizing carbon footprint and summary
        HTML2canvas for pdf 

How to setup the project in Windows, Mac and Linux
   1.requirements 
     Python 3.8 should be installed in respective machine
     Git should be installed
     Git bash app installed  terminal for Windows 
     Terminal for Linux or Mac
     (Git Bash(software app for insatlling Git) or terminal will work for Linux or Mac)
    
    2. Clone the repository 
        git clone  git@github.com:jithin6384/carbonEmissionCalculatorTool.git
        cd carbonEmissionCalculatorTool

    3. Setup Local requirement
      On windows
         python -m venv env
         env/Scripts/activate (to activate the virtual enviroment)
      On Linux/MacOs
         python -m venv env
         source  env/bin/activate (to activate the virtual enviroment)
    4. Install requirements(from requirements.txt)
         pip install -r requirements.txt
    
    5. Initialize the database:
         flask db init
         flask db migrate
         flask db upgrade
    6.set the FLASK_APP 
        export FLASK_APP=app.py (for Linux/MacOS)
        set FLASK_APP=app.py (for Windows)
    7. Run the app in Local
       python3 app.py


    live url: https://carbonemissioncalculatortool.onrender.com/register (set using in Render.com)
              http://198.199.83.64:8000/register deployed using digital ocean droplet 
 8. Example charts generated using javascript and python are attached in this carbon_data.pdf and globalcorp_carbon_data.html
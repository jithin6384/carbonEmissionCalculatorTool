from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Carbon Footprint Monitoring Tool!"

@app.route('/adminPage')
def adminTool():
    return "Welcome to admin page its in construction once ready you can see the summaries of carbon footprints of different companies logged in here.."

if __name__ == '__main__':
    app.run(debug=True)

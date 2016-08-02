"""Script for launching and maintaing the web page."""
from flask import Flask
app = Flask(__name__)


#  Main Landing Page:
@app.route('/')
def landing_page():
    """Display the landing page."""
    with open('index.html') as indx:
        return indx.read()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

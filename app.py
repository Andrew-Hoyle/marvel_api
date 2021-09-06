from flask import Flask, render_template
from marvel_inventory import routes

if __name__ == "__main__":
    app.run(debug=True)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

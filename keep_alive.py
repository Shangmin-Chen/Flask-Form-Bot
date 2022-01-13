from flask import Flask, render_template, request
from threading import Thread
from replit import db

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
  if request.method == "POST":
    fname = request.form["First"]
    lname = request.form["Last"]
    email = request.form["Mail"]
    print("New user registered: {} {} {}".format(fname, lname, email))
    if "database" in db.keys():
      database = db["database"]
      data = [fname, lname, email]
      database.append(data)
      db["database"] = database
      return "You are added to the database! See you at 6 tomorrow :)"
    else:
      database = []
      data = [[fname, lname, email]]
      db["database"] = data
      return "You're the first!"


def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

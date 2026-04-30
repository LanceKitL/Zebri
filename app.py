from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import Quest

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/")
def home():
    return render_template('home.html')

# add a route for the ff.
# show quests (get) 
@app.route('/show_quest', methods=["GET"])
def show_quest(): 
    show_quests = Quest.select()
    return render_template("./quests/index.html", quests = show_quests)

# add quest (post)
@app.route('/add_quest', methods=["POST", "GET"])
def add_quest():
    if request.method == "POST":
        quest = Quest.create(
            title = request.form['title'],
            description = request.form['description'],
            difficulty = request.form['difficulty'],
        )

        if not quest: 
            flash("Failed, Please check your input.", "Error")
            return redirect("/")

        flash("Quest Added", "Success")
        return redirect(url_for("show_quest"))
    
    return render_template('./quests/create.html')

# updating quest (put)

@app.route("/get_quest/<int:id>", methods=["GET"])
def get_quest(id):
    quest = Quest.get_by_id(id)
    
    # safety check
    if not quest:
        flash("Quest Doesnt Exist","Error")
        return redirect("/")
    
    return render_template("./quests/show.html", quest=quest)

if __name__ == "__main__":
    app.run(debug=True)
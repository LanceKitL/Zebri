from flask import Flask, render_template, request, redirect, url_for
from models import Quest

app = Flask(__name__)


@app.route("/")
def index():
    quests = Quest.select()
    return render_template('index.html', quests=quests)


@app.route("/add_quest", methods=["POST"])
def add_quest():
    Quest.create(
        title=request.form['title'],
        description=request.form['description'],
        difficulty=request.form['difficulty']
    )
    
    return redirect('/')


@app.route("/complete/<int:id>")
def complete(id):
    quest = Quest.get_by_id(id)
    quest.is_completed = True
    quest.save()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
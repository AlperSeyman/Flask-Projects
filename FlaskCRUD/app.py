from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from extensions import db
from models import MyTask

app = Flask(__name__)
Scss(app)


# Database

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)

#Home Page
@app.route("/", methods=["POST","GET"])
def index():
    # Add a Task
    if request.method == "POST":
        current_task = request.form.get("content")
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
    # See all tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template("home.html", tasks=tasks)


# Delete Task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error: {e}"

# Update Task
@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form.get("content")
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("update.html", task=task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
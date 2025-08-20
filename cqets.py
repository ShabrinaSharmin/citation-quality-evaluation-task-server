from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory user and task storage
users = {
    "user1@cqets.com": {"password": "user1pass", "first_name": "John"}
}

tasks = []

# ====== LOGIN ======
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users.get(email)
        if user and user["password"] == password:
            session["user_email"] = email
            session["user_first_name"] = user["first_name"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


# ====== DASHBOARD ======
@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user_first_name=session["user_first_name"])


# ====== ADD TASK ======
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if "user_email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        task_name = request.form["task_name"]
        dataset = request.form["dataset"]
        tasks.append({"task_name": task_name, "dataset": dataset})
        return render_template("task_success.html", task_name=task_name, dataset=dataset)
    
    return render_template("add_task.html")


# ====== VIEW TASKS ======
@app.route("/view_tasks")
def view_tasks():
    if "user_email" not in session:
        return redirect(url_for("login"))
    return render_template("view_tasks.html", tasks=tasks)


# ====== LOGOUT ======
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
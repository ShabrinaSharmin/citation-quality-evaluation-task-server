from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory storage for users and tasks
users = {
    "alice@cqets.com": {"password": generate_password_hash("password123"), "first_name": "Alice", "user_id" : "1"},
    "bob@cqets.com": {"password": generate_password_hash("secret456"), "first_name": "Bob", "user_id" : "2"},
}

TASKS_FILE = 'dummy_tasks.json'

# Load tasks from JSON
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save tasks to JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# -------------------- Login --------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and check_password_hash(users[email]["password"], password):
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password")
    return render_template("login.html")

# -------------------- Dashboard --------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    user_email = session["user"]
    first_name = users[user_email]["first_name"]
    return render_template("dashboard.html", first_name=first_name)

# -------------------- Add Task --------------------
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Read all form fields
        task_name = request.form["task_name"]
        model_name = request.form["model_name"]
        huggingface_key = request.form["huggingface_key"]  
        wandb_key = request.form["wandb_key"]
        eval_type = request.form["eval_type"]
        compute_ip = request.form["compute_ip"]
        user_login = request.form["user_login"]
        certificate_text = request.form["certificate_text"]  # now a string from textarea
        emails = request.form["emails"]

        if not all([task_name, model_name, huggingface_key, wandb_key, eval_type, compute_ip, user_login, certificate_text]):
            return render_template("add_task.html", error="Please fill all mandatory fields")


        # Prepare task dictionary
        task = {
            "task_name": task_name,
            "model_name": model_name,
            "evaluation_type": eval_type,
            "compute_ip": compute_ip,
            "compute_user": user_login,
            "certificate_text": certificate_text,  # store but not display
            "additional_emails": emails,
            "status" : "Not Started"
        }

        all_tasks= load_tasks()

        # Add to user's task list
        user_email = session["user"]
        if user_email not in all_tasks:
            all_tasks[user_email] = []
        all_tasks[user_email].append(task)

        #save the file
        save_tasks(all_tasks)

        # Redirect to success page with submitted info (safe fields only)
        return render_template("task_success.html", task=task)

    return render_template("add_task.html")

# -------------------- View Tasks --------------------
@app.route("/view_tasks")
def view_tasks():
    if "user" not in session:
        return redirect(url_for("login"))
    user_email = session["user"]
    tasks = load_tasks()
    user_tasks = tasks.get(user_email, [])
    return render_template("view_tasks.html", tasks=user_tasks, user_email=user_email)

# -------------------- View Results --------------------
@app.route("/view_results/<email>/<task_name>")
def view_results(email, task_name):
#     # Check if email exists in tasks

#     tasks = load_tasks()
#     email = email
#     user_tasks = tasks.get(user_email, [])
#     if not user_tasks:
#         return "User or tasks not found", 404

#     # Find the task with the given ID
#     task = next((t for t in tasks if t['id'] == task_id), None)
#     if not task:
#         return "Task not found", 404

#     # Get the task results
#     results = results_data.get(email, {}).get(task_id, {})
#     if not results:
#         return "Results not available yet", 404

    return render_template('view_results.html')#, task=task, results=results, email=email)


# -------------------- Logout --------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))




if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
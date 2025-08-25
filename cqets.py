from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from asqa import ASQA
from qampari import QAMPARI
from eli5 import ELI5
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory storage for users and tasks
users = {
    "alice@cqets.com": {"password": generate_password_hash("alice123"), "first_name": "Alice", "user_id" : "1"},
    "bob@cqets.com": {"password": generate_password_hash("bob123"), "first_name": "Bob", "user_id" : "2"},
}
RESULTS_FOLDER = "./results/"
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

#loads the json results file
def load_result_file(email, task_id):
    """Load the JSON file for a specific task."""
    filename = f"{email}_task_{task_id}.json"
    filepath = os.path.join(RESULTS_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

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
        task_id = ""
        # Add to user's task list
        user_email = session["user"]
        if user_email in all_tasks:
            task_id = str(len(all_tasks[user_email])+1)
        else:
            all_tasks[user_email] = []
            task_id = str(1)
        task["task_id"] = task_id
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
@app.route("/view_results/<email>/<task_id>")
def view_results(email, task_id):
    results_path = os.path.join(RESULTS_FOLDER, f"{email}_task_{task_id}.json")
    if not os.path.exists(results_path):
        return f"No results found for task {task_id} and user {email}", 404

    with open(results_path) as f:
        results = json.load(f)
        view_results ={}
        view_results["model_name"] = results.get("model_name", "")
        if "ASQA" in results:
            asqa = ASQA(results["ASQA"]["str_em"], results["ASQA"]["citation_rec"], results["ASQA"]["citation_prec"])
            view_results["ASQA"] = asqa.to_dict()
        if "QAMPARI" in results:
            qampari = QAMPARI(results["QAMPARI"]["qampari_rec_top5"], results["QAMPARI"]["qampari_prec"], results["QAMPARI"]["citation_rec"], results["QAMPARI"]["citation_prec"])
            view_results["QAMPARI"] = qampari.to_dict()
        if "ELI5" in results:
            eli5 = ELI5(results["ELI5"]["claims_nli"], results["ELI5"]["citation_prec"], results["ELI5"]["citation_rec"])
            view_results["ELI5"] = eli5.to_dict()
    return render_template(
        "view_results.html",
        email=email,
        taskid=task_id,
        result=view_results
        )

# -------------------- Compare Results --------------------
@app.route("/compare_results",  methods=["GET", "POST"])
def compare_results():
    if "user" not in session:
        return redirect(url_for("login"))

    user_email = session["user"]
    # List all task files for this user
    result_files = [f for f in os.listdir(RESULTS_FOLDER) if f.startswith(f"{user_email}_task_") and f.endswith(".json")]
    task_options = []
    for f in result_files:
        task_id = f.replace(f"{user_email}_task_", "").replace(".json", "")
        try:
            data = load_result_file(user_email, task_id)
            model_name = data.get("model_name", "")
            task_options.append({"task_id": task_id, "model_name": model_name})
        except:
            continue

    # Get selected tasks from query params
    task1_id = request.args.get("task1")
    task2_id = request.args.get("task2")
    comparison = None
    task1_model_name = ""
    task2_model_name = ""

    if task1_id and task2_id:
        task1 = load_result_file(user_email, task1_id)
        task2 = load_result_file(user_email, task2_id)
        comparison = {}
        task1_model_name = task1["model_name"]
        task2_model_name = task2["model_name"]

        for metric in task1:
            if metric == "model_name":
                continue

            if isinstance(task1[metric], dict):
                comparison[metric] = {}
                if metric == "ASQA":
                    asqa_task1 = ASQA(task1[metric]["str_em"], task1[metric]["citation_rec"], task1[metric]["citation_prec"])
                    asqa_task2 = ASQA(task2.get(metric, {}).get("str_em", 0), task2.get(metric, {}).get("citation_rec", 0), task2.get(metric, {}).get("citation_prec", 0) )
                    asqa_task1_dict = asqa_task1.to_dict()
                    asqa_task2_dict = asqa_task2.to_dict()
                    for item in asqa_task1.to_dict():
                        comparison["ASQA"][item] = {"val1": asqa_task1_dict[item], "val2": asqa_task2_dict[item], "delta": abs(asqa_task1_dict[item] - asqa_task2_dict[item])}
                if metric == "QAMPARI":
                    qampari_task1 = QAMPARI(task1[metric]["qampari_rec_top5"], task1[metric]["qampari_prec"], task1[metric]["citation_rec"], task1[metric]["citation_prec"])
                    qampari_task2 = QAMPARI(task2.get(metric, {}).get("qampari_rec_top5", 0), task2.get(metric, {}).get("qampari_prec", 0), task2.get(metric, {}).get("citation_rec", 0), task2.get(metric, {}).get("citation_prec", 0) )
                    qampari_task1_dict = qampari_task1.to_dict()
                    qampari_task2_dict = qampari_task2.to_dict()
                    for item in qampari_task1.to_dict():
                        comparison["QAMPARI"][item] = {"val1": qampari_task1_dict[item], "val2": qampari_task2_dict[item], "delta": abs(qampari_task1_dict[item] - qampari_task2_dict[item])}
                if metric == "ELI5":
                    eli5_task1 = ELI5(task1[metric]["claims_nli"], task1[metric]["citation_prec"], task1[metric]["citation_rec"])
                    eli5_task2 = ELI5(task2.get(metric, {}).get("claims_nli", 0), task2.get(metric, {}).get("citation_prec", 0), task2.get(metric, {}).get("citation_rec", 0) )
                    eli5_task1_dict = eli5_task1.to_dict()
                    eli5_task2_dict = eli5_task2.to_dict()
                    for item in eli5_task1.to_dict():
                        comparison["ELI5"][item] = {"val1": eli5_task1_dict[item], "val2": eli5_task2_dict[item], "delta": abs(eli5_task1_dict[item] - eli5_task2_dict[item])}

                # for sub_metric in task1[metric]:
                #     val1 = task1[metric][sub_metric]
                #     val2 = task2.get(metric, {}).get(sub_metric, 0)
                #     delta = float(val1) - float(val2)
                #     comparison[metric][sub_metric] = {"val1": val1, "val2": val2, "delta": abs(delta)}
            # else:
            #     val1 = task1[metric]
            #     val2 = task2.get(metric, 0)
            #     delta = float(val2) - float(val1)
            #     comparison[metric] = {"val1": val1, "val2": val2, "delta": delta}

    return render_template("compare_results.html",
                           task_options=task_options,
                           comparison=comparison,
                           task1_id=task1_id,
                           task2_id=task2_id,
                           task1_model_name = task1_model_name,
                           task2_model_name = task2_model_name)

# -------------------- Logout --------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))




if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
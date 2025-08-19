from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for sessions

# Dummy credentials
USER_DATA = {"user@cqets.com": "password123"}


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if USER_DATA.get(email) and USER_DATA[email] == password:
            session["user"] = email  # Store logged-in user in session
            return redirect(url_for("task_form"))
        else:
            error = "Invalid email or password."
    return render_template("login.html", error=error)

@app.route("/task", methods=["GET", "POST"])
def task_form():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Get form data
        task_name = request.form.get("task_name")
        dataset = request.form.get("dataset")

        # Pass data to success page
        return render_template("task_success.html", task_name=task_name, dataset=dataset)

    return render_template("task_form.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
from flask import render_template, url_for, flash, redirect

from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm


posts = [
    {
    'title': 'The last of the mohicans',
    'author': 'steven spelberg',
    'date_posted': 'Jan 8, 1995',
    'content': 'First post content'
},
{
    'title': 'Facing mount Kenya',
    'author': 'Jomo Kenyatta',
    'date_posted': 'March 8, 1943',
    'content': 'Second post content'
}
]
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        app.logger.debug("Form validated successfully.")
        flash(f"Account created for {form.username.data}!", "success")
        app.logger.debug("Redirecting to home route")  # Add this line for debugging
        return redirect(url_for("login"))
    
    app.logger.debug("Form validation failed")  # Add this line for debugging
    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "abc@xyz.com" and form.password.data == "password":
            flash("Signed in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Incorrect details!", "danger")

    return render_template("login.html", title="login", form=form)

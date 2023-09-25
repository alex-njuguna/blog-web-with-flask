from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateUserForm
from flaskblog.models import User, Post
from flaskblog import bcrypt


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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        app.logger.debug("Form validated successfully.")
        # encrypt password
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        # save new user to db
        # with app.app_context():
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! Sign in.", "success")
        app.logger.debug("Redirecting to home route")  # Add this line for debugging
        return redirect(url_for("login"))
    
    app.logger.debug("Form validation failed")  # Add this line for debugging
    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash("Signed in successfully!", "success")
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("home"))
            else:
                flash("Incorrect details!", "danger")
        else:
            flash("User does not exist!", "danger")
    return render_template("login.html", title="login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your details have been updated successfully!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="/profile_pics/"+current_user.image_file)
    return render_template("account.html", title="account", image_file=image_file, form=form)


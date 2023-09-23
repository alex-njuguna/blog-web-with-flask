from datetime import datetime

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "1a4d297629d8174a611dfd27e8b2f640"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User: {self.username}, Email: {self.email} Image: {self.image_file}"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"{self.title}, {self.date_posted}"


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


if __name__ == "__main__":
    app.run(debug=True)
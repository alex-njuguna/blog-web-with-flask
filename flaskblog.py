from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "1a4d297629d8174a611dfd27e8b2f640"

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


@app.route("/login")
def login():
    form = LoginForm()

    return render_template("login.html", title="login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        app.logger.debug("Redirecting to home route")  # Add this line for debugging
        return redirect(url_for("home"))
    app.logger.debug("Form validation failed")  # Add this line for debugging
    return render_template("register.html", title="register", form=form)


if __name__ == "__main__":
    app.run(debug=True)
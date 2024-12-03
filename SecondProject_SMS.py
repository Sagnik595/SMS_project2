



from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, login_required, logout_user, current_user)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(100), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"


with app.app_context():
     db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Route for home page after login
@app.route("/home1")
@login_required
def home1():
    if current_user.first_name == "SagnikS" and current_user.last_name == "Sagnik":
        students = User.query.all()
        return render_template("home1.html", students=students)
    else:
        return redirect(url_for("login"))


@app.route("/home2")
def home2():
    return render_template("home2.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        roll_no = request.form.get("roll")
        course = request.form.get("course")
        address = request.form.get("address")
        mobile = request.form.get("mobile")
        dob = request.form.get("dob")
        password = request.form.get("password")

        if first_name and last_name and roll_no and course and address and mobile and dob:
            existing_user = User.query.filter_by(roll_no=roll_no).first()
            if existing_user:
                flash("User with this roll number already exists.", "error")
                return redirect(url_for("register"))

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                roll_no=roll_no,
                course=course,
                address=address,
                mobile=mobile,
                dob=dob,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for("home1"))
        else:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))

    return render_template("register1.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(first_name=username).first()

        # Check for admin credentials
        if username == "SagnikS" and password == "12345":
            return redirect(url_for("home1"))
        elif user and user.password == password:
            login_user(user)
            flash("Student logged in!", "success")
            return redirect(url_for("home2"))
        else:
            flash("Invalid credentials!", "error")

    return render_template("login.html")


@app.route('/student_login_button', methods=['POST'])
def student_login_button():
    return redirect(url_for('login'))


@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome to your dashboard, {current_user.first_name}!"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/delete_student/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    if current_user.first_name == "SagnikS":
        student = User.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully!", "success")
        return redirect(url_for("home1"))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))


@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    if current_user.first_name == "SagnikS":
        student = User.query.get_or_404(student_id)
        if request.method == "POST":
            student.first_name = request.form.get("first_name")
            student.last_name = request.form.get("last_name")
            student.roll_no = request.form.get("roll_no")
            student.course = request.form.get("course")
            student.address = request.form.get("address")
            student.mobile = request.form.get("mobile")
            student.dob = request.form.get("dob")
            db.session.commit()
            flash("Student details updated successfully!", "success")
            return redirect(url_for("home1"))

        return render_template("edit_student.html", student=student)
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))


@app.route('/check_schema')
def check_schema():
    result = db.session.execute("PRAGMA table_info(user);")
    schema = [{"column_id": row[0], "name": row[1], "type": row[2], "not_null": row[3]} for row in result]
    return {"schema": schema}


@app.route('/home')
def home():
    return render_template('home1.html')


if __name__ == "__main__":
    app.run(debug=True)

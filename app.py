from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, flash

from flask_sqlalchemy import SQLAlchemy
# from wtforms.fields import form

# from forms import LoginForm, RegisterForm

# from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

# Now create flask application object

app = Flask(__name__)

# Database Configuration and Creating object of SQLAlchemy

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create User Model which contains id [Auto Generated], name, username, email and password


class User(db.Model):

    __tablename__ = 'usertable'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(15), unique=True)

    username = db.Column(db.String(15), unique=True)

    email = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(256), unique=True)


class Notes(db.Model):

    sno = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    textarea = db.Column(db.String(500), nullable=False)

    td = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# @app.route('/')
# def home():
#     return render_template('index.html')

# User Registration Api End Point


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     # Creating RegistrationForm class object
#     form = RegisterForm(request.form)

#     # Cheking that method is post and form is valid or not.
#     if request.method == 'POST' and form.validate():

#         # if all is fine, generate hashed password
#         hashed_password = generate_password_hash(
#             form.password.data, method='sha256')

#         # create new user model object
#         new_user = User(

#             name=form.name.data,

#             username=form.username.data,

#             email=form.email.data,

#             password=hashed_password)

#         # saving user object into data base with hashed password
#         db.session.add(new_user)

#         db.session.commit()

#         flash('You have successfully registered', 'success')

#         # if registration successful, then redirecting to login Api
#         return redirect(url_for('login'))

#     else:

#         # if method is Get, than render registration form
#         return render_template('register.html', form=form)

# # Login API endpoint implementation


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     # Creating Login form object
#     form = LoginForm(request.form)
#     # verifying that method is post and form is valid
#     if request.method == 'POST' and form.validate:
#         # checking that user is exist or not by email
#         user = User.query.filter_by(email=form.email.data).first()

#         if user:
#             # if user exist in database than we will compare our database hased password and password come from login form
#             if check_password_hash(user.password, form.password.data):
#                 # if password is matched, allow user to access and save email and username inside the session
#                 flash('You have successfully logged in.', "success")

#                 session['logged_in'] = True

#                 session['email'] = user.email

#                 session['username'] = user.username
#                 # After successful login, redirecting to home page
#                 # return redirect(url_for('home'))
#                 return render_template('notes.html')

#             else:

#                 # if password is in correct , redirect to login page
#                 flash('Username or Password Incorrect', "Danger")

#                 return redirect(url_for('login'))
#     # rendering login page
#     return render_template('login.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def add_notes():
    if request.method == 'POST':
        title = request.form['title']
        textarea = request.form['textarea']

        if not title and not textarea:
            error_statement = " Fields are required "
            return render_template('notes.html', error_statement=error_statement, title=title, textarea=textarea)

        note = Notes(title=title, textarea=textarea)
        db.session.add(note)
        db.session.commit()
        flash('Note added!', category='success')

    allTodo = Notes.query.all()
    return render_template('notes.html', allTodo=allTodo)


@app.route('/show')
def show():
    allTodo = Notes.query.all()
    print(allTodo)
    return render_template('show.html', allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        textarea = request.form['textarea']

        # if not title and textarea:
        #     update_statement = "Notes update successfully"
        #     return render_template('update.html' , update_statement = update_statement , title = title , textarea = textarea)

        note = Notes.query.filter_by(sno=sno).first()
        note.title = title
        note.textarea = textarea
        db.session.add(note)
        db.session.commit()
        return redirect("/show")

    note = Notes.query.filter_by(sno=sno).first()
    return render_template('update.html', note=note)


@app.route('/delete/<int:sno>')
def delete(sno):
    note = Notes.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()
    return redirect("/show")


@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return render_template('login.html')


if __name__ == '__main__':
    # Creating database tables
    db.create_all()
    # running server
    app.run(debug=True, port="5008")

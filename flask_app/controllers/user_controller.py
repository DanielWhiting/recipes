from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User 
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.recipe_model import Recipe


bcrypt = Bcrypt(app)
# bcrypt.generate_password_hash(password_string)
# bcrypt.check_password_hash(hashed_password, password_string)

@app.route('/')
def home():
  return redirect('/login')

# If they are logged in it will redirect them to the dashboard

@app.route('/login')
def login():
  if 'user_id' in session:
    return redirect('/dashboard')
  return render_template('login.html')

#creating a new user with validation and hashing the password

@app.route('/add/user', methods = ['POST'])
def register():
  if not User.validate(request.form):
    return redirect('/login')
  hashed_pw = bcrypt.generate_password_hash(request.form['password'])
  data = {
    **request.form,
    'password': hashed_pw
  }
  session['user_id'] = User.add_user(data) # Make sure to always instantiate the data!
  return redirect('/dashboard')

#If a person is not in session than kick them out. If they are in session than render the page

@app.route('/dashboard')
def dashboard():
  if not 'user_id' in session:
    return redirect('/')
  user = User.get_by_id({'id':session['user_id']}) # queston on this 
  all_recipes = Recipe.get_all()
  return render_template('dashboard.html', user = user, all_recipes = all_recipes)

#removing session from the person when they logout so they will have to log back in

@app.route('/logout')
def logout():
  del session['user_id']
  return redirect('/')

#Validating login informating making sure it matches the one stored in the database

@app.route('/users/login', methods=['POST'])
def user_login():
  data = {
    'email': request.form['email']
  }
  user_from_db = User.get_email(data)
  if not user_from_db:
    flash("Invalid Credentials", 'log')
    return redirect('/login')
  if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
    flash("invalid Credentials", 'log')
    return redirect('/login')
  session['user_id'] = user_from_db.id
  return redirect('/dashboard')

# route for displaying just my recipes

@app.route('/my_recipes')
def my_recipes ():
  if not 'user_id' in session:
    return redirect('/')
  user = User.my_stuff({'id':session['user_id']})
  return render_template('my_stuff.html', user = user)
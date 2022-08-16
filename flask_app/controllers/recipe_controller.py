from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app import app

@app.route('/create/recipe')
def new_recipe():
  if not 'user_id' in session:
    return redirect('/')
  user = User.get_by_id({'id':session['user_id']})
  return render_template('recipe_new.html', user = user)
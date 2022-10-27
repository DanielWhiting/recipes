from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_app import app

# Path for our current user to make a recipe, session checks by id

@app.route('/create/recipe')
def new_recipe():
  if not 'user_id' in session:
    return redirect('/')
  user = User.get_by_id({'id':session['user_id']})
  return render_template('recipe_new.html', user = user)

#adding to our recipes

@app.route('/new/recipe', methods=['POST'])
def add_recipe():
  if not 'user_id' in session:
    return redirect('/')
  print(request.form)
  if not Recipe.recipe_valid(request.form):
    return redirect('/create/recipe')
  data = {
    **request.form,
    'user_id': session['user_id']
  }
  Recipe.add_recipe(data)
  return redirect('/dashboard')

  # Edit your recipe but not anyone elses

@app.route('/recipe/<int:id>/edit')
def edit_recipe(id):
  if not 'user_id' in session:
    return redirect('/')
  recipe = Recipe.get_by_id({'id': id})
  return render_template('recipe_edit.html', recipe = recipe)

  # Submitting our edit form updating the information

@app.route('/recipe/<int:id>/update', methods=['POST'])
def update_recipe(id):
  if not 'user_id' in session:
    return redirect('/')
  print(request.form)
  if not Recipe.recipe_valid(request.form):
    return redirect(f'/recipe/{id}/edit')
  data = {
    **request.form,
    'id': id
  }
  Recipe.update(data)
  return redirect('/dashboard')

  # deleting your own recipe

@app.route('/recipe/<int:id>/delete')
def delete_recipe(id):
  if not 'user_id' in session:
    return redirect('/')
  data = {
    'id': id
  }
  to_be_deleted = Recipe.get_by_id(data)
  #this protects from other users deleting other users items
  if not session['user_id'] == to_be_deleted.user_id:
    flash('Cant delete other users items')
    return redirect('/dashboard')
  Recipe.delete(data)
  return redirect('/dashboard')

  # To view one recipe at a time

@app.route('/recipe/<int:id>')
def show_one_recipe(id):
  if not 'user_id' in session:
    return redirect('/dashboard')
  data = {
    'id': id
  }
  show = Recipe.get_by_id(data)
  user = User.get_by_id({'id':session['user_id']})
  return render_template('view_recipe.html', show = show, user = user)
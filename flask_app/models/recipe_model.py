from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model


class Recipe:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.description = data['description']
    self.instructions = data['instructions']
    self.date = data['date']
    self.under_30 = data['under_30']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']

  # Inserting recipes into the database
  @classmethod
  def add_recipe(cls, data):
      query = "INSERT INTO recipes (name, description, instructions, date, under_30, user_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(date)s,%(under_30)s, %(user_id)s);"
      result = connectToMySQL('recipe').query_db(query,data)
      return result
      
  # Updating database
  @classmethod
  def update(cls, data):
    query = "UPDATE recipes SET name = %(name)s,description = %(description)s,instructions = %(instructions)s,date = %(date)s,under_30 = %(under_30)s WHERE id = %(id)s;"
    result = connectToMySQL('recipe').query_db(query, data)
    return result

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM recipes JOIN user ON user.id = recipes.user_id;" 
    #This is critical for displaying make sure join is right or will get user id error
    result = connectToMySQL('recipe').query_db(query)
    if result:
      all_recipes = []
      for row in result:
        this_recipe = cls(row) #why do we only put id, and created, and updated?
        user_data = {
          **row,
          'id': row['user.id'],
          'created_at': row['user.created_at'],
          'updated_at': row['user.updated_at']
        }
        this_user = user_model.User(user_data)
        this_recipe.posted_by = this_user #posted by is a new attribute
        all_recipes.append(this_recipe)
      return all_recipes
    return result

  # get one method to match id so people cant delete other users recipses used with delete method


  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM recipes JOIN user ON user.id = recipes.user_id WHERE recipes.id = %(id)s"
    result = connectToMySQL('recipe').query_db(query, data)
    if len(result) < 1:
      return False
    row = result[0]
    this_recipe = cls(row)
    user_data = {
      **row,
      'id': row['user.id'],
      'created_at': row['user.created_at'],
      'updated_at': row['user.created_at']
    }
    this_user = user_model.User(user_data)
    this_recipe.this_user = this_user  #this user is a new attribute
    return this_recipe

    # delete recipe method working with above method get_by_id
  @classmethod
  def delete(cls, data):
    query = "DELETE FROM recipes WHERE id = %(id)s"
    return connectToMySQL('recipe').query_db(query, data)
    

  # Validating recipe information

  @staticmethod
  def recipe_valid(form_data):
    is_valid = True
    if len(form_data['name']) < 1:
      flash('Name Required', 'rec')
      is_valid = False
    if len(form_data['description']) < 1:
      flash('Need a decription', 'rec')
      is_valid = False
    if len(form_data['instructions']) < 1:
      flash('Need instructions', 'rec')
      is_valid = False
    if len(form_data['date']) < 1:
      flash('Date Required', 'rec')
      is_valid = False
    if 'under_30' not in form_data:
      flash('Under 30 minutes required', 'rec')
      is_valid = False
    return is_valid
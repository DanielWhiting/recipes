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

  # Inserting receipes into the database
  @classmethod
  def add_user(cls, data):
      query = "INSERT INTO recipes (name, description, instructions, date, under_30) VALUES(%(name)s,%(description)s,%(instructions)s,%(date)s,%(under_30)s);"
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
    query = "SELECT * FROM user JOIN recipes ON user_id = user.id;"
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
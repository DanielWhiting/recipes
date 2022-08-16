from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import DATABASE

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
  def __init__(self, data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  # need a classmethod to insert new users into our database

  @classmethod
  def add_user(cls, data):
      query = "INSERT INTO user (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
      result = connectToMySQL('recipe').query_db(query,data)
      return result

  # getting the email and checking its length    
      
  @classmethod
  def get_email(cls, data):
    query = "SELECT * FROM user WHERE email = %(email)s;"
    result = connectToMySQL('recipe').query_db(query,data)
    if len(result) < 1:
        return False
    return cls(result[0])

  # Get one user to display name

  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM user WHERE id = %(id)s"
    result = connectToMySQL('recipe').query_db(query, data)
    if len(result) < 1:
      return False
    return cls(result[0])

  # Validating name, email, and password
  @staticmethod
  def validate(user_data):
    is_valid = True
    if len(user_data['first_name']) < 2:
      is_valid = False
      flash('First name must be longer than 2 characters', 'reg')
    if len(user_data['last_name']) < 2:
      is_valid = False
      flash('Last name must be longer than 2 characters', 'reg')
    if len(user_data['email']) < 1:
      is_valid = False
      flash('Please provide email', 'reg')
    elif not EMAIL_REGEX.match(user_data['email']):
      is_valid = False
      flash('Invalid email', 'reg')
    else:
      data = {
        'email': user_data['email']
      }
      potential_user = User.get_email(data)
      if potential_user:
        is_valid = False
        flash('Email already exists','reg')
    if len(user_data['password']) < 8:
      is_valid = False
      flash('Password must be at least 8 characters', 'reg')
    elif not user_data['password'] == user_data['confirm_pass']:
      flash('Password does not match', 'reg')
      is_valid = False
    return is_valid
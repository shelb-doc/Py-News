from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

import sys

bp = Blueprint('api', __name__, url_prefix='/api')

#Api Routes
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()
  try:
    # attempt creating a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    db.add(newUser)
    db.commit()
  except:
    print(sys.exc_info()[0])
  # insert failed, so rollback and send error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  # Session log
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

# logout
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

# login
@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = 'Incorrect credentials'), 400

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  return jsonify(id = user.id)
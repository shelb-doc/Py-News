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
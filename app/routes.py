from flask import Blueprint, request, jsonify

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return jsonify(message="Welcome to the Bug Tracker API"), 200
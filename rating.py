from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models import db, Movie, Rating

rating_bp = Blueprint('rating', __name__, url_prefix='/api/rating')

@rating_bp.route('/create', methods=['POST'])
@login_required
def create_rating():
    data = request.get_json()
    movie_id = data['movie_id']
    value = data['value']

    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({'error': 'Invalid movie ID'})

    rating = Rating(movie=movie, user=current_user, value=value)
    db.session.add(rating)
    db.session.commit()

    return jsonify({'success': 'Rating created successfully'})

@rating_bp.route('/list', methods=['GET'])
def list_ratings():
    movie_id = request.args.get('movie_id')

    if not movie_id:
        return jsonify({'error': 'Missing movie ID'})

    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({'error': 'Invalid movie ID'})

    ratings = [r.to_dict() for r in movie.ratings]

    return jsonify({'ratings': ratings})

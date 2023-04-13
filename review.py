from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models import db, Movie, Review

review_bp = Blueprint('review', __name__, url_prefix='/api/review')

@review_bp.route('/create', methods=['POST'])
@login_required
def create_review():
    data = request.get_json()
    movie_id = data['movie_id']
    text = data['text']

    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({'error': 'Invalid movie ID'})

    review = Review(movie=movie, user=current_user, text=text)
    db.session.add(review)
    db.session.commit()

    return jsonify({'success': 'Review created successfully'})

@review_bp.route('/list', methods=['GET'])
def list_reviews():
    movie_id = request.args.get('movie_id')

    if not movie_id:
        return jsonify({'error': 'Missing movie ID'})

    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({'error': 'Invalid movie ID'})

    reviews = [r.to_dict() for r in movie.reviews]

    return jsonify({'reviews': reviews})

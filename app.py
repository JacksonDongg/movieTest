from flask import Flask, request, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['db']
ratings = db['Ratings']
reviews = db['Reviews']

#
# @app.route('/', methods=['GET'])
# def home():
# return "Welcome to the TV Shows Rating and Comment system!"

# Create or update a rating record
@app.route('/ratings', methods=['POST'])
def create_or_update_rating():
    data = request.get_json()
    tv_series_id = data['TVSeriesId']
    user_id = data['UserId']
    rating = data['Rating']
    # Check if the rating record already exists
    existing_rating = ratings.find_one({'TVSeriesId': tv_series_id, 'UserId': user_id})
    if existing_rating is None:
        # Create a new rating record
        rating_id = ratings.insert_one({'TVSeriesId': tv_series_id, 'UserId': user_id, 'Rating': rating}).inserted_id
    else:
        # Update an existing rating record
        ratings.update_one({'_id': existing_rating['_id']}, {'$set': {'Rating': rating}})
        rating_id = existing_rating['_id']
    return str(rating_id)

# Create or update a review record
@app.route('/reviews', methods=['POST'])
def create_or_update_review():
    data = request.get_json()
    tv_series_id = data['TVSeriesId']
    user_id = data['UserId']
    review = data['Review']
    # Check if the review record already exists
    existing_review = reviews.find_one({'TVSeriesId': tv_series_id, 'UserId': user_id})
    if existing_review is None:
        # Create a new review record
        review_id = reviews.insert_one({'TVSeriesId': tv_series_id, 'UserId': user_id, 'Review': review}).inserted_id
    else:
        # Update an existing review record
        reviews.update_one({'_id': existing_review['_id']}, {'$set': {'Review': review}})
        review_id = existing_review['_id']
    return str(review_id)

# Get a rating record
@app.route('/ratings/<int:user_id>/<int:tv_series_id>', methods=['GET'])
def get_rating(user_id, tv_series_id):
    # Find the rating record for the user and TV series
    rating = ratings.find_one({'TVSeriesId': tv_series_id, 'UserId': user_id})
    if rating is not None:
        # Convert the rating record to JSON and return it
        return jsonify({'TVSeriesId': rating['TVSeriesId'], 'UserId': rating['UserId'], 'Rating': rating['Rating']})
    else:
        return 'Rating not found', 404

# Get a review record
@app.route('/reviews/<int:user_id>/<int:tv_series_id>', methods=['GET'])
def get_review(user_id, tv_series_id):
    # Find the review record for the user and TV series
    review = reviews.find_one({'TVSeriesId': tv_series_id, 'UserId': user_id})
    if review is not None:
        # Convert the review record to JSON and return it
        return jsonify({'TVSeriesId': review['TVSeriesId'], 'UserId': review['UserId'], 'Review': review['Review']})
    else:
        return 'Review not found', 404

if __name__ == '__main__':
    app.run(debug=True)

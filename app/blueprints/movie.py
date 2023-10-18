from flask import Blueprint, request,jsonify
from app.models import MovieModel
from app.extensions import db

bp_movie = Blueprint('bp_movie',__name__)

@bp_movie.route('/api/allMovies')
def index():
    movies = MovieModel.query.all()
    movie_list = [movie.to_dict() for movie in movies]
    return jsonify(movie_list)

@bp_movie.route('/api/movies/projection', methods=['GET'])
def get_winner_info():
    #Query winner movies
    winner_movies = MovieModel.query.filter_by(winner='yes').order_by(MovieModel.producers, MovieModel.year).all()

    # Group movies by producers
    producer_movies = {}
    for movie in winner_movies:
        if movie.producers not in producer_movies:
            producer_movies[movie.producers] = []
        producer_movies[movie.producers].append(movie)

    min_intervals = []
    max_intervals = []

    # Find minimum and maximum intervals for each producer with at least two winner movies
    for producer, movies in producer_movies.items():
        if len(movies) >= 2:
            intervals = [(movies[i + 1].year - movies[i].year, movies[i], movies[i + 1]) for i in range(len(movies) - 1)]
            min_interval = min(intervals, key=lambda x: x[0])
            max_interval = max(intervals, key=lambda x: x[0])
            min_intervals.append({
                'producer': producer,
                'interval': min_interval[0],
                'previousWin': min_interval[1].year,
                'followingWin': min_interval[2].year
            })
            max_intervals.append({
                'producer': producer,
                'interval': max_interval[0],
                'previousWin': max_interval[1].year,
                'followingWin': max_interval[2].year
            })

    result = {
        'min': min_intervals,
        'max': max_intervals
    }

    response_data = {
        'message': 'Intervals fetched successfully.',
        'data': result
    }

    return jsonify(response_data), 200





@bp_movie.route('/api/movies/',methods=['POST'])
def store():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify(error="Invalid JSON data"), 400

    for movie_data in data:
        year = movie_data.get('year')
        title = movie_data.get('title')
        studios = movie_data.get('studios')
        producers= movie_data.get('producers')
        winner= movie_data.get('winner')


        new_movie = MovieModel(title=title, year=year,studios = studios,producers=producers,winner=winner)
        db.session.add(new_movie)

    db.session.commit()

    return jsonify(message="Movies added successfully"), 201


@bp_movie.route('/api/movies/<int:id>', methods=['GET'])
def show_movie(id):
    movie = MovieModel.query.get_or_404(id).to_dict()
    return jsonify(movie)

@bp_movie.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = MovieModel.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie deleted successfully'}), 200
    else:
        return jsonify({'message': 'Movie not found'}), 404
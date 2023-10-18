from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    db.init_app(app)


    @app.route('/')
    def main():
        return "API is running..."

    from app.blueprints import movie
    app.register_blueprint(movie.bp_movie)

    # Post CSV movies automatically
    import csv
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    try:
        with open('movielist.csv', 'r', encoding='utf-8') as file:
            csvreader = csv.DictReader(file, delimiter=';')
            for row in csvreader:
                movie_data = {
                    'year': row['year'],
                    'title': row['title'],
                    'studios': row['studios'],
                    'producers': row['producers'],
                    'winner': row['winner']
                }

                try:
                    session = requests.Session()
                    retry = Retry(connect=3, backoff_factor=0.5)
                    adapter = HTTPAdapter(max_retries=retry)
                    session.mount('http://', adapter)
                    response = session.post('http://localhost:5000/api/movies', json=movie_data)
                    response.raise_for_status()
                    print(f"Movie {movie_data['title']} posted successfully.")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to post movie {movie_data['title']}: {e}")

    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

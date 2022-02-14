from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from all_schemas import DirectorsSchema, GenresSchema, MoviesSchema
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api=Api(app)
movies_ns=api.namespace('movies')
genres_ns=api.namespace('genres')
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

@movies_ns.route("/")
class Movies_view(Resource):
    def get(self):
        movies_schema=MoviesSchema(many=True)
        director_id=request.args.get('director_id')
        genre_id=request.args.get('genre_id')
        if director_id and genre_id:
            movies=Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        elif director_id:
            movies=Movie.query.filter_by(director_id=director_id).all()
        elif genre_id:
            movies = Movie.query.filter_by(genre_id=genre_id).all()
        else:
            movies=Movie.query.all()
        if movies:
            return movies_schema.dump(movies), 200
        else: return "", 404
    def post(self):
        pass


@movies_ns.route("/<int:uid>")
class Movie_view(Resource):
    def get(self, uid:int):
        movie=Movie.query.get(uid)
        if movie:
            movie_schema=MoviesSchema()
            return movie_schema.dump(movie), 200
        else: return "", 404


@genres_ns.route("/")
class genres_view(Resource):
    def get(self):
        genres_schema = GenresSchema(many=True)
        genres=Genre.query.all()
        if genres:
            return genres_schema.dump(genres), 200
        else: return "", 404


    def post(self):
        req_json=request.json
        new_genre=Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genres_ns.route("/<int:uid>")
class genre_view(Resource):
    def get(self, uid:int):
        genre = Genre.query.get(uid)
        if genre:
            genres_schema = GenresSchema()
            return genres_schema.dump(genre), 200
        else: return "", 404
    def put(self, uid:int):
        genre=Genre.query.get(uid)
        if genre:
            req_json=request.json
            genre.name=req_json.get('name')
            db.session.add(genre)
            db.session.commit()
            return "", 201
        else: return "", 404


if __name__ == '__main__':
    app.run()
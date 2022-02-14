from marshmallow import fields, Schema


class MoviesSchema(Schema):
    id=fields.Int(dump_only=True)
    title=fields.Str()
    description=fields.Str()
    trailer=fields.Str()
    year=fields.Int()
    rating=fields.Int()
    genre_id=fields.Int()
    director_id=fields.Int()


class DirectorsSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()

class GenresSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()

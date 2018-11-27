from app import db

class ORMClass(object):
    @classmethod
    def query(cls):
        return db.session.query(cls)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        rv = cls.get(id)
        if rv is None:
            abort(404)
        return rv

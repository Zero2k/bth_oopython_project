#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Database ORM
"""

from flask import abort
from app import db

class ORMClass(object):
    """ ORM Class """

    @classmethod
    def create(cls, **kw):
        """ Create entity """
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def update(cls, obj):
        """ Update entity """
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def delete(cls, obj):
        """ Delete entity """
        db.session.delete(obj)
        db.session.commit()

    @classmethod
    def query(cls):
        """ Query entity """
        return db.session.query(cls)

    @classmethod
    def get(cls, entity_id):
        """ Get entity with ID """
        return cls.query.get(entity_id)

    @classmethod
    def get_or_404(cls, entity_id):
        """ Create entity with ID or 404 """
        rv = cls.query.get(entity_id)
        if rv is None:
            abort(404)
        return rv

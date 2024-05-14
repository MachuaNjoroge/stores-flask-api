from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainTagSchema, TagSchema

from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import TagModel, StoreModel




blp = Blueprint("tag", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"] ).first():
            abort(400, message="A tag with that name already exists for this store" )

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return tag

    
    @blp.response(204)
    def delete(self, tag_id):
        store = TagModel.query.get_or_404(tag_id)
        db.session.delete(store)
        db.session.commit()
    
    @blp.arguments(PlainTagSchema)
    @blp.response(200, PlainTagSchema)
    def put(cls, store_data, tag_id):
        store = TagModel.query.get_or_404(tag_id)

        if store:
            store.name = store_data["name"]
        else:
           store = TagModel(id=tag_id,**store_data)

        db.session.add(store)
        db.session.commit()

        return store
       


@blp.route("/tag/<string:tag_id>")
class Store(MethodView):

    @blp.response(200,TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        
 
  
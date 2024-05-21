from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jwt

from schemas import PlainTagSchema, TagSchema, TagAndItemSchema

from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import TagModel, StoreModel, ItemTagsModel, ItemModel




blp = Blueprint("tag", __name__, description="Operations on tags")


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

    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self, tag_id):

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

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
       


@blp.route("/tag/<int:tag_id>")
class TagsById(MethodView):

    @blp.response(200,TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202,
                  description="Deletes a tag if no item is tagged with it",
                  example={"message": "Tag deleted."},)
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Returned if this tag is assigned to one or more items. In this case, the tag is not deleted.",)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        
        abort(400, message="Could not delete tag. Make sure that thag is associated with any items and try again.")


    @jwt_required(fresh=True)
    @blp.arguments(PlainTagSchema)
    @blp.response(201, PlainTagSchema)
    def put(self, tag_data, tag_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        tag = TagModel.query.get_or_404(tag_id)

        try:
            tag.name = tag_data["name"]
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message=f"Error updating tag {tag}")
        
        return tag
            
            

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class ItemTags(MethodView):

    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return tag

    @jwt_required(fresh=True)
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return {"message": "Item removed from tag", "item": item, "tag": tag}
  

@blp.route("/tag")
class Tags(MethodView):

    @jwt_required()
    @blp.response(200, PlainTagSchema(many=True))
    def get(self):
        return TagModel.query.all()
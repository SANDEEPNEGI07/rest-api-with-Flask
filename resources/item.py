from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel, TagModel, StoreModel
from db import db
from schemas import ItemSchema, ItemUpdatSchema

#import name = __name__, name of blueprint = stores
blp = Blueprint("Items", __name__, description="Operations on Items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin priviliage required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message":"Item deleted"}

    @blp.arguments(ItemUpdatSchema)
    @blp.response(200, ItemSchema)
    #item_data will go as the first argument beacause the valid data will be passed to the first argument in the function.
    # Put is idempotant, means updating once or 10 times means the same.
    def put(self, item_data, item_id ):
        item = ItemModel.query.get(item_id)
        
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # Get store by ID
        store = StoreModel.query.get_or_404(item_data["store_id"])
        # Get or create tags by names
        tags = []
        if "tag_names" in item_data:
            for name in item_data["tag_names"]:
                tag = TagModel.query.filter_by(name=name).first()
                if not tag:
                    tag = TagModel(name=name, store_id=store.id)
                    db.session.add(tag)
                    db.session.commit()
                tags.append(tag)

        # Remove used fields from item_data
        item_data.pop("store_id")
        item_data.pop("tag_names", None)

        item = ItemModel(**item_data, store=store, tags=tags)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item

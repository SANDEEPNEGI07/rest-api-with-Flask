import uuid
from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel

from schemas import StoreSchema

#import name = __name__, name of blueprint = stores
blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store/<int:store_id>")
class Stores(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
            
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists."
            )
        except SQLAlchemyError:
            abort(500, messgae="An error occured while Creating Store.")

        return store
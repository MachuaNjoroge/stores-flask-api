from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema

from blocklist import BLOCKLIST

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt, get_jwt_identity

from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import UserModel

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegistration(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201)
    def post(self, user_data):
        # if UserModel.query.filter(UserModel.username == user_data["username"].first()):
        #     abort(409, message="User already exists!!")
        username = user_data["username"]
        password = pbkdf2_sha256.hash(user_data["password"])
        user = UserModel(username=username, password=password)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error creating user")
        return {"message": "user created successfully"}
    

    @blp.route("/login")
    class UserLogin(MethodView):

        @blp.arguments(UserSchema)
        @blp.response(202)
        def post(self,user_data):
            user_cursor = UserModel.query.filter(UserModel.username == user_data["username"]).first()
            if not user_cursor:
                abort(401, messaga="invalid username or password")
            
            # Verify that the password supplied is the same as the one in user.password
            if user_cursor and pbkdf2_sha256.verify(user_data["password"],user_cursor.password):
                access_token = create_access_token(identity=user_cursor.id, fresh=True)
                refresh_token = create_refresh_token(identity=user_cursor.id)
                
                return {"access token": access_token, "refresh_token": refresh_token}
            abort(401, message="Invalid credentials")


    @blp.route("/refresh")
    class UserRefresh(MethodView):

        @jwt_required(refresh=True)
        @blp.response(200)
        def post(self):
            identiy = get_jwt_identity()
            new_token = create_access_token(fresh=False, identity=identiy)
            return new_token




@blp.route("/user/<int:user_id>")
class Users(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(204)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit(user)
        except SQLAlchemyError:
            abort(500, message="Error deleting user")
        
        return {"message": "User deleted successfully"}
    

@blp.route("/logut")
class Logout(MethodView):

    @jwt_required()
    @blp.response(200)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User successfully loggout out."}

            
            
    

        

from flask import Flask, render_template, request, redirect
from config import Config
from app.extensions import db, migrate, jwt
from app.services.user_validation import UserValidation, fetch_joke
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, set_access_cookies,unset_jwt_cookies

def create_app():

    app = Flask(__name__ ,static_url_path="", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

   
    @app.route("/", methods=["GET","POST"])
    def index():
        if request.method == "POST":

            data = {
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
                "confirm": request.form.get("confirm_password"),
                "address": request.form.get("address"),
                "hobbies": request.form.getlist("hobbies"),
                "gender": request.form.get("gender"),
                "terms": request.form.get("terms")
            }

            msg, error, status = UserValidation.register_validation(data)

            if error:
                return error

            return redirect("/login")

        return render_template("index.html")


    @app.route("/login", methods=["GET","POST"])
    def login():

        if request.method == "POST":

            data = {
                "email": request.form.get("email"),
                "password": request.form.get("password")
            }

            res, error, status = UserValidation.login_validation(data)

            if error:
                return error

            token = res["access_token"]

            response = redirect("/dashboard")
            set_access_cookies(response, token)

            return response

        return render_template("login.html")


    @app.route("/dashboard")
    @jwt_required()
    def dashboard():

        joke = fetch_joke()
        return render_template("dashboard.html",
                               joke=joke)


    @app.route("/logout")
    @jwt_required()
    def logout():
        response = redirect("/")
        unset_jwt_cookies(response)
        return response
    
    return app

if __name__=="__main__":
    create_app()
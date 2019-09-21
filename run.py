import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://"
app.config["SQLALCHEMY_DATABASE_URI"] = "{}".format(os.getenv('DATABASE_URL'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "some-secret-string"

db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
jwt = JWTManager(app)

app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

import views, models, resources

api.add_resource(resources.UserRegistration, "/registration")
api.add_resource(resources.UserLogin, "/login")
api.add_resource(resources.UserLogoutAccess, "/logout/access")
api.add_resource(resources.GetLicence, "/licence/<string:bot_id>")
api.add_resource(resources.WriteLicenceTime, "/writelicencetime")
api.add_resource(resources.GetMessages, "/messages")
api.add_resource(resources.UpdateBotHash, "/updatehash")
api.add_resource(resources.FlushBotHash, "/flushhash")
api.add_resource(resources.BotLogin, "/botlogin")
api.add_resource(resources.BotLogoutAccess, "/botlogout/access")
api.add_resource(resources.SaveStartPaymentData, "/payments")
api.add_resource(resources.GetPayment, "/getpayment/<string:url_safe>")
api.add_resource(resources.UpdatePaymentData, "/updatepayment")


#if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)

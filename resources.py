from flask_restful import Resource, reqparse
from models import UserModel, InfoAdvMessages, PaymentsModel
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
import json
import datetime as dt
from cryptography.fernet import Fernet


class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)
        parser.add_argument("bot_hash", help="This field cannot be blank", required=True)
        parser.add_argument("bot_licence", help="", required=False)
        parser.add_argument("secret_for_bot_registration", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_for_bot_reg = "LXORWIiKFXUSBO2Ip_sVKpRByuwDVhSOt9nTgopUoQ8="

        if UserModel.find_by_bot_id(data["bot_id"]):
            return {"message": "User {} already exists".format(data["bot_id"])}

        new_user = UserModel(
            bot_hash=data["bot_hash"],
            bot_id=data["bot_id"],
            bot_licence=data["bot_licence"],
            reg_date=str(dt.datetime.utcnow()),
        )

        try:
            if data["secret_for_bot_registration"] == secret_for_bot_reg:

                new_user.save_to_db()
                access_token = create_access_token(identity=data["bot_id"])
                return {
                    "message": "User {} was created".format(data["bot_id"]),
                    "access_token": access_token,
                }
        except:
            return {"message": "Something went wrong"}, 500


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        current_user = UserModel.find_by_bot_id(data["bot_id"])

        if not current_user:
            return {"message": "User {} doesn't exist".format(data["bot_id"])}

        if UserModel.find_by_bot_id(data["bot_id"]):
            licence_dict = UserModel.return_bot_licence(data["bot_id"])
            licence_time_encrypted = licence_dict["users"][0]["bot_licence"]

            if licence_time_encrypted != None:
                secret_for_encruption_licence_time = "CAQRzbEvyDxfy-h3Nk-fURRWlzuzneygxSCMLfv2vsY="
                key = secret_for_encruption_licence_time + data["bot_id"]
                f = Fernet(key)
                licence_time_encrypted = licence_time_encrypted.encode()
                x = f.decrypt(licence_time_encrypted)
                x = x.decode()
                licence_time_for_human = x[:19]

                return {
                    "message": "Logged in as {}".format(current_user.bot_id),
                    "licence_valid_until": licence_time_for_human,
                }

            else:
                return {
                    "message": "Logged in as {}".format(current_user.bot_id),
                    "licence_valid_until": "licence doesn't exist",
                }
        else:
            return {"message": "Wrong credentials"}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        return {"message": "Something went wrong"}, 500



class BotLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)
        parser.add_argument("secret_for_bot_login", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_login_bot = "Jrp-_Xipu6xFdYrp_9RDK5Ur3wDUI16J0nc0spbRvE0="

        current_user = UserModel.find_by_bot_id(data["bot_id"])

        if not current_user:
            return {"message": "User {} doesn't exist".format(data["bot_id"])}

        if UserModel.find_by_bot_id(data["bot_id"]) and data["secret_for_bot_login"] == secret_login_bot:
            access_token = create_access_token(identity=data["bot_id"])
            return {
                "message": "Logged in as {}".format(current_user.bot_id),
                "access_token": access_token,
            }
        else:
            return {"message": "Wrong credentials"}


class BotLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        return {"message": "Something went wrong"}, 500



class GetLicence(Resource):
    @jwt_required
    def get(self, bot_id):
        if UserModel.find_by_bot_id(bot_id):
            x = UserModel.return_bot_licence(bot_id)
            return x
        else:
            return "bot_id not found"


class GetMessages(Resource):
    def get(self):
        m = InfoAdvMessages.get_messages()
        return m



class GetPayment(Resource):
    @jwt_required
    def get(self, url_safe):
        if PaymentsModel.find_by_url_safe(url_safe):
            x = PaymentsModel.get_payment(url_safe)
            return x
        else:
            return "url_safe not found"


class UpdateBotHash(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)
        parser.add_argument("bot_hash", help="This field cannot be blank", required=True)
        parser.add_argument("secret_for_write_hash", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_write_hash = "K_z1Lter7c-33tr76jUujXEqIU12uP1UsAYAcyPgZ5A="

        if UserModel.find_by_bot_id(data["bot_id"]) and data["secret_for_write_hash"] == secret_write_hash:
            user_to_write = UserModel.find_by_bot_id(data["bot_id"])
            if user_to_write.bot_hash == None:

                user_to_write.bot_hash = data["bot_hash"]
                user_to_write.update_on_db()
                return "ok"

            else:
                return "write error, bot_hash exists"

        else:
            return "write error"



class FlushBotHash(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)
        parser.add_argument("secret_for_flush_bot_hash", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_flush = "qsh-pPXIvoK1L6sCTgI3JyyOw3U5GLcUSfCTS2sz3Vc="

        if UserModel.find_by_bot_id(data["bot_id"]) and data["secret_for_flush_bot_hash"] == secret_flush:
            user_to_write = UserModel.find_by_bot_id(data["bot_id"])
            user_to_write.bot_hash = None
            user_to_write.update_on_db()
            return "ok"
        else:
            return "write error"



class WriteLicenceTime(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)
        parser.add_argument("bot_licence", help="This field cannot be blank", required=True)
        parser.add_argument("secret_for_write_bot_licence", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_write_date = "JqeL56RwnbVgmrloN1Du-FkF0wAVSBZ6i55v5rN0eZU="

        if UserModel.find_by_bot_id(data["bot_id"]) and data["secret_for_write_bot_licence"] == secret_write_date:
            user_to_write = UserModel.find_by_bot_id(data["bot_id"])
            user_to_write.bot_licence = data["bot_licence"]
            user_to_write.update_on_db()
            return "ok"
        else:
            return "write error"



class SaveStartPaymentData(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=True)
        parser.add_argument("url_safe", help="This field cannot be blank", required=True)
        parser.add_argument("secret_for_save_payment", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_for_save_payment = "59rjZ73apdw833ucC2mJNpmX5gvrYmLPHHx-OYh9C3I="

        new_payment = PaymentsModel(
            bot_id=data["bot_id"],
            url_safe=data["url_safe"],
            date=str(dt.datetime.utcnow()),

        )

        try:
            if data["secret_for_save_payment"] == secret_for_save_payment:

                new_payment.save_to_db()
                return {
                    "message": "save payment ok",
                }
        except:
            return {"message": "Something went wrong"}, 500



class UpdatePaymentData(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bot_id", help="This field cannot be blank", required=False)
        parser.add_argument("url_safe", help="This field cannot be blank", required=True)
        parser.add_argument("transaction_hash", help="This field cannot be blank", required=False)
        parser.add_argument("address", help="This field cannot be blank", required=False)
        parser.add_argument("value", help="This field cannot be blank", required=False)
        parser.add_argument("callback_provider", help="This field cannot be blank", required=False)
        parser.add_argument("currency", help="This field cannot be blank", required=False)
        parser.add_argument("secret_for_update_payment", help="This field cannot be blank", required=True)

        data = parser.parse_args()
        secret_for_update_payment = "jFjoALtajZzA6ZFXw_Yw7kRDbNNUuQa3_MzPL2d8BKY="

        if PaymentsModel.find_by_url_safe(data["url_safe"]) and data["secret_for_update_payment"] == secret_for_update_payment:

            url_safe_to_write = PaymentsModel.find_by_url_safe(data["url_safe"])

            if url_safe_to_write.transaction_hash == None:
                url_safe_to_write.transaction_hash = data["transaction_hash"]
            if url_safe_to_write.address == None:
                url_safe_to_write.address = data["address"]
            if url_safe_to_write.value == None:
                url_safe_to_write.value = data["value"]
            if url_safe_to_write.callback_provider == None:
                url_safe_to_write.callback_provider = data["callback_provider"]
            if url_safe_to_write.currency == None:
                url_safe_to_write.currency = data["currency"]

            url_safe_to_write.update_date = str(dt.datetime.utcnow())

            url_safe_to_write.update_on_db()
            return "ok"


        else:
            return "write error"

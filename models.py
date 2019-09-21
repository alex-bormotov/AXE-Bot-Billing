from run import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    bot_hash = db.Column(db.String(), unique=False)
    bot_id = db.Column(db.String(), nullable=False, unique=True)
    bot_licence = db.Column(db.String())
    reg_date = db.Column(db.String())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_on_db(self):
        db.session.commit()

    @classmethod
    def find_by_bot_hash(cls, bot_hash):
        return cls.query.filter_by(bot_hash=bot_hash).first()

    @classmethod
    def find_by_bot_id(cls, bot_id):
        return cls.query.filter_by(bot_id=bot_id).first()

    @classmethod
    def return_bot_licence(cls, bot_id):
        def to_json(x):
            return {"bot_licence": x.bot_licence, "bot_hash": x.bot_hash}

        return {
            "users": list(
                map(lambda x: to_json(x), UserModel.query.filter_by(bot_id=bot_id))
            )
        }

    @classmethod
    def return_bot_id(cls, bot_id):
        def to_json(x):
            return {"bot_id": x.bot_id}

        return {
            "users": list(
                map(lambda x: to_json(x), UserModel.query.filter_by(bot_id=bot_id))
            )
        }


class InfoAdvMessages(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String())
    adv = db.Column(db.String())


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_on_db(self):
        db.session.commit()

    @classmethod
    def get_messages(cls):
        def to_json(x):
            return {"info": x.info, "adv": x.adv}

        return {
            "messages": list(
                map(lambda x: to_json(x), InfoAdvMessages.query.all())
            )
        }



class PaymentsModel(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.String(), nullable=False)
    url_safe = db.Column(db.String(), nullable=False, unique=True)
    transaction_hash = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=True)
    callback_provider = db.Column(db.String(), nullable=True)
    currency = db.Column(db.String(), nullable=True)
    date = db.Column(db.String())
    update_date = db.Column(db.String())


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_on_db(self):
        db.session.commit()

    @classmethod
    def find_by_url_safe(cls, url_safe):
        return cls.query.filter_by(url_safe=url_safe).first()


    @classmethod
    def get_payment(cls, url_safe):
        def to_json(x):
            return {"url_safe": x.url_safe, "bot_id": x.bot_id, "value": x.value, "transaction_hash": x.transaction_hash}

        return {
            "payments": list(
                map(lambda x: to_json(x), PaymentsModel.query.filter_by(url_safe=url_safe))
            )
        }

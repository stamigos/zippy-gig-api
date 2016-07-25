# -*- coding: utf8 -*-
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from peewee import (Model, CharField, TextField, ForeignKeyField, IntegerField, SmallIntegerField,
                    DateTimeField, DoubleField, BooleanField, datetime as peewee_datetime)

from playhouse.pool import PooledPostgresqlExtDatabase

from config import DB_CONFIG, SECRET_KEY
from utils import get_random_string
from zippy_gig.constants import AccountType

db = PooledPostgresqlExtDatabase(**DB_CONFIG)
db.commit_select = True
db.autorollback = True

peewee_now = peewee_datetime.datetime.now


class _Model(Model):
    class Meta:
        database = db


class Account(_Model):
    class Meta:
        db_table = "accounts"

    email = CharField(unique=True, max_length=320)
    password = CharField()
    created = DateTimeField(default=peewee_now)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    address = CharField(null=True)
    phone = CharField(null=True)
    alt_phone = CharField(null=True)
    pay_pal = CharField(null=True)
    avatar = CharField(null=True)
    type = SmallIntegerField(null=True)

    def __repr__(self):
        return "{class_name}(id={id})".format(class_name=self.__class__.__name__, id=self.id)

    def to_dict(self):
        return dict(self._data.items())

    def get_data(self):
        data = dict(self._data.items())
        data.pop("password")
        return data

    def get_profile(self):
        profile_data = ["first_name", "last_name", "address",
                        "phone", "alt_phone", "pay_pal"]
        return {key: item for key, item in self._data.items() if key in profile_data}

    @staticmethod
    def get_vendors():
        return Account.select().where(Account.type == AccountType.Vendor)

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        account = Account.get(Account.id == data['id'])
        return account

    # def get_clients(self):
    #     return self.select().where(self.type == AccountType.Client)


def init_db():
    try:
        db.connect()
        map(lambda l: db.drop_table(l, True),
            [Account]
            )
        print "tables dropped"
        [m.create_table() for m in [Account]]
        print "tables created"
        account = Account(email="test@example.com",
                          password="123",
                          first_name="Vitalii")
        account.save()
    except:
        db.rollback()
        raise


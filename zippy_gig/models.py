# -*- coding: utf8 -*-
import os
from hashlib import sha1
from werkzeug.utils import secure_filename

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from peewee import (Model, CharField, TextField, ForeignKeyField, IntegerField, SmallIntegerField,
                    DateTimeField, DoubleField, BooleanField, datetime as peewee_datetime)

from playhouse.pool import PooledPostgresqlExtDatabase
from flask import Markup, request


from config import DB_CONFIG, SECRET_KEY, MEDIA_ROOT, MEDIA_URL
from zippy_gig.constants import AccountType

db = PooledPostgresqlExtDatabase(**DB_CONFIG)
db.commit_select = True
db.autorollback = True

peewee_now = peewee_datetime.datetime.now


class _Model(Model):
    class Meta:
        database = db


class Photo(_Model):
    class Meta:
        db_table = "photos"

    image = CharField(null=True)

    def __unicode__(self):
        return self.image

    def save_image(self, file_obj):
        self.image = secure_filename(file_obj.filename)
        full_path = os.path.join(MEDIA_ROOT, self.image)
        file_obj.save(full_path)
        self.save()

    def url(self):
        return os.path.join(MEDIA_URL, self.image)

    def thumb(self):
        return Markup('<img src="%s" style="height: 80px;" />' % self.url())


class Account(_Model):
    """
        Provider/Client account model
    """
    class Meta:
        db_table = "accounts"

    email = CharField(unique=True, max_length=320)
    password = CharField()
    created = DateTimeField(default=peewee_now)
    first_name = CharField(null=True, max_length=255)
    last_name = CharField(null=True, max_length=255)
    address = TextField(null=True)
    phone = CharField(null=True)
    alt_phone = CharField(null=True)  # alternative phone
    pay_pal = CharField(null=True)
    avatar = ForeignKeyField(Photo, null=True)
    type = SmallIntegerField(null=True)  # account type: 1|2|3

    # provider's specific fields
    zip_code = CharField(null=True)

    def __repr__(self):
        return "{class_name}(id={id})".format(class_name=self.__class__.__name__, id=self.id)

    def to_dict(self):
        return dict(self._data.items())

    def get_data(self):
        data = dict(self._data.items())
        data.pop("password")
        data.update({"job_types": self.get_job_types()})
        data.update({"avatar_url": self.avatar.url() if self.avatar else None})
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

    def get_job_types(self):
        query = JobType.select().join(AccountJobType).join(Account).where(Account.id == self.id)
        return [job.title for job in query]

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

    def upload_photo(self):
        if 'avatar' in request.files:
            _file = request.files['avatar']
            photo = Photo.create(image=_file.filename)
            photo.save_image(_file)
            self.avatar = photo
            self.save()


class JobType(_Model):
    """
        Job type model
    """
    class Meta:
        db_table = "job_types"

    title = CharField()


class AccountJobType(_Model):
    """
        Model with many-to-many relation:
         jobs that providers able to do
    """
    class Meta:
        db_table = "accounts_job_types"

    account = ForeignKeyField(Account, related_name="job_type_accounts")
    job_type = ForeignKeyField(JobType, related_name="account_job_types")


def init_db():
    try:
        db.connect()
        map(lambda l: db.drop_table(l, True),
            [AccountJobType, Account, JobType, Photo]
            )
        print "tables dropped"
        [m.create_table() for m in [Photo, Account, JobType, AccountJobType]]
        print "tables created"
        job_types = ['Websites design', 'Marketing', 'Plumbing', 'Babysitter', 'Grocery Shopping',
                     'Fast Food/conveniences delivery', 'Maid service', 'Painting', 'Yardwork', 'Home repairs',
                     'Personal shopper', 'Pet Grooming', 'Pet sitting', 'Dog Walker', 'Notary Services',
                     'Legal Services', 'Writing', 'Translations', 'Beauty/Salon services', 'Automotive Repair',
                     'Bartending/Foodservice', 'Cooks/chef/baker (cakes)', 'Blogger', 'Outbound Call Agent',
                     'Photographer', 'Music Bands', 'Computer Aid', 'Tailor', 'Accounting/Tax', 'Psychic',
                     'Marriage Officiant', 'Exterminator', 'Pool repairs/maintenance',
                     'Odd Ball Gigs (profiles can add these jobs)',
                     'Cell phone Help', 'Nursing Aids', 'Performers', 'Tutors']
        for jb in job_types:
            with db.transaction():
                JobType.create(title=jb)

        account = Account(email="test@example.com",
                          password=sha1("123").hexdigest(),
                          first_name="test",
                          last_name="last_name")
        account.save()
    except:
        db.rollback()
        raise


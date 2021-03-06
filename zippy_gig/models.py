# -*- coding: utf8 -*-
import os
from hashlib import sha1
from werkzeug.utils import secure_filename

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from peewee import (Model, CharField, TextField, ForeignKeyField, IntegerField, SmallIntegerField,
                    DateTimeField, DoubleField, BooleanField, DecimalField, datetime as peewee_datetime,
                    fn)

from playhouse.pool import PooledPostgresqlExtDatabase
from flask import Markup, request, g


from config import DB_CONFIG, SECRET_KEY, MEDIA_ROOT, MEDIA_URL
from zippy_gig.constants import AccountType

from geopy.geocoders import Nominatim

db = PooledPostgresqlExtDatabase(**DB_CONFIG)
db.commit_select = True
db.autorollback = True

import zippy_gig.sql_additional

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


# to set zip_code use only set_zip_code method!
class Account(_Model):
    """
        Provider/Client account model
    """
    class Meta:
        db_table = "accounts"

    email = CharField(unique=True, max_length=320)
    password = CharField()
    is_active = BooleanField(default=True)
    created = DateTimeField(default=peewee_now)
    first_name = CharField(null=True, max_length=255)
    last_name = CharField(null=True, max_length=255)
    address = TextField(null=True)
    phone = CharField(null=True)
    alt_phone = CharField(null=True)  # alternative phone
    pay_pal = CharField(null=True)
    avatar = ForeignKeyField(Photo, null=True)
    type = SmallIntegerField(null=True, default=3)  # account type: 1 - client | 2 - vendor | 3 - both
    zip_code = CharField(null=True)
    lng = DecimalField(null=True)
    lat = DecimalField(null=True)

    # provider's specific fields
    vendor_status = SmallIntegerField(null=True)  # 1 - in | 2 - out
    vendor_description = TextField(null=True)

    def __repr__(self):
        return "{class_name}(id={id})".format(class_name=self.__class__.__name__, id=self.id)

    def to_dict(self):
        return dict(self._data.items())

    def get_data(self):
        data = dict(self._data.items())
        print data
        data.pop("password")
        data.update({"job_types": self.get_job_types()})
        data.update({"avatar_url": self.avatar.url() if self.avatar else None})
        return data

    def get_profile(self):
        profile_data = ["first_name", "last_name", "address",
                        "phone", "alt_phone", "pay_pal", "type", "zip_code"]
        data = {key: item for key, item in self._data.items() if key in profile_data}
        data.update({"avatar_url": self.avatar.url() if self.avatar else None})
        data.update({"job_types": self.get_job_types()})
        return data

    @staticmethod
    def get_vendors(job_type=None, vendor_status=None, account_id=None, account_type=None,
                    radius=None):
        condition = ((Account.type == AccountType.Vendor.value)\
                     | (Account.type == AccountType.ClientAndVendor.value))

        if account_type in {AccountType.Vendor.value, AccountType.ClientAndVendor.value}:
            condition &= (Account.id != account_id)

        if radius is not None:
            condition &= (fn.distance_kilometers(g.account.lat, g.account.lng, Account.lat, Account.lng) <= radius)


        _ret_val = Account.select().where(condition)

        # TODO: change querying. .join() ?
        if job_type is not None:
            _ret_val = _ret_val.select()\
                .where(Account.id << [item.account.id for item in AccountJobType.select().where(AccountJobType.job_type == job_type)])

        if vendor_status is not None:
            _ret_val = _ret_val.select().where(Account.vendor_status == vendor_status)

        return _ret_val

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    def get_job_types(self):
        query = JobType.select().join(AccountJobType).join(Account).where(Account.id == self.id)
        return [{'id': job.id, 'title': job.title} for job in query]

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
            return os.path.join(MEDIA_URL, photo.image)
        return None

    def set_zip_code(self, _zip_code):
        self.zip_code = _zip_code

        geo_locator = Nominatim()
        location = geo_locator.geocode(self.zip_code)
        if location:
            self.lat = location.latitude
            self.lng = location.longitude
        else:
            self.lat = None
            self.lng = None

        del geo_locator


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


class Gig(_Model):
    """
        Work Model
    """
    class Meta:
        db_table = "gig"

    _type = ForeignKeyField(JobType, related_name="work_type")
    description = TextField(null=True)
    price = IntegerField(null=True)
    account = ForeignKeyField(Account, related_name="work_type_accounts")

    def get_gig(self):
        return {key: item for key, item in self._data.items()}


def init_db():
    try:
        db.connect()
        map(lambda l: db.drop_table(l, True),
            [Gig, AccountJobType, Account, JobType, Photo]
            )
        print "tables dropped"
        [m.create_table() for m in [Photo, Account, JobType, AccountJobType, Gig]]
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
                          last_name="last_name",
                          )
        account.set_zip_code("04116")
        account.save()

    except:
        db.rollback()
        raise


def fill_db():
    zip_codes = ['01135', '50055', '01032']

    for i in range(1, 4):
        print i
        email = 'test%d@example.com' % i
        password = sha1("123").hexdigest()
        first_name = "test%d" % i
        last_name = "last_name%d" % i

        zip_code = zip_codes[i-1]

        if i % 3:
            vendor_status = '1'
        else:
            vendor_status = '2'
        type = 2
        account = Account(email=email,
                          password=password,
                          first_name=first_name,
                          last_name=last_name,
                          vendor_status=vendor_status,
                          type=type)
        account.set_zip_code(zip_code)
        account.save()

    for j in range(1, 5):
        account_job_type = AccountJobType(account=Account.select().where(Account.id == j),
                                          job_type=JobType.select().where(JobType.id == j))

        account_job_type.save()


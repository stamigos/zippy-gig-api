from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import db, Account
from zippy_gig.utils import hash_pswd


class SignUpController(BaseController):
    def __init__(self, request):
        super(SignUpController, self).__init__(request)

    def _call(self):
        email = self._verify_field("email")
        password = self._verify_field("password")
        return self._create_account(email, password).to_dict()

    def _create_account(self, email, password):
        email = self._check_account(email)
        with db.transaction():
            account = Account.create(email=email,
                                     password=hash_pswd(password),
                                     type=self._check_account_type())
        return account

    def _check_account(self, email):
        try:
            Account.get(Account.email == email)
            raise ApiException("Email %s already registered" % email)
        except Account.DoesNotExist:
            return email

    def _check_account_type(self):
        account_type = self._verify_field("account_type")
        try:
            return int(account_type)
        except ValueError:
            raise ApiException("Incorrect account type")







"""Initialization tests"""
import unittest

from booking_host_api.booking import Booking
from booking_host_api.base import InvalidParameterError, AuthenticationError
from .common import BasicBookingTesting, write_private_data_to_file, get_OTP_from_input
from .common import some_not_registered_email, blocked_account_email, some_password, some_ses, some_cookies, some_account_id

class TestBookingCredentialsInit(BasicBookingTesting):
    """
        Positive tests of initialization with Selenium.
        
        Provide json file ("tests/private_data.json" by default, see common.PRIVATE_DATA_FILE_PATH) with 
        valid email and password. See tests/private_data_template.json for structure of a private data file. 
        test_init_basic and test_init_otp, if succeeded, write ses, cookies and account_id values to json file.
    """
    @classmethod
    def setUpClass(cls):
        cls.read_private_data_to_class('email', 'password')

    def test_init_basic(self):
        api = Booking(email=self.email, password=self.password)
        ses_value = api.access_ses()
        cookies_value = api.access_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, cookies_value, account_id_value)
        write_private_data_to_file(ses=ses_value, cookies=cookies_value, account_id=account_id_value)
        
    def test_init_otp(self):
        api = Booking(email=self.email, password=self.password, OTP=get_OTP_from_input)
        ses_value = api.access_ses()
        cookies_value = api.access_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, cookies_value, account_id_value)
        write_private_data_to_file(ses=ses_value, cookies=cookies_value, account_id=account_id_value)

    def test_init_with_account_id(self):
        api = Booking(email=self.email, password=self.password, account_id=some_account_id)
        ses_value = api.access_ses()
        cookies_value = api.access_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, cookies_value, account_id_value)
        self.assertEqual(some_account_id, account_id_value, f'account_id was set to {account_id_value}, expected {some_account_id}')

    def test_init_otp_with_account_id(self):
        api = Booking(email=self.email, password=self.password, account_id=some_account_id, OTP=get_OTP_from_input)
        ses_value = api.access_ses()
        cookies_value = api.access_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, cookies_value, account_id_value)
        self.assertEqual(some_account_id, account_id_value, f'account_id was set to {account_id_value}, expected {some_account_id}')


class TestBookingAuthDataInit(BasicBookingTesting):
    """Positive tests of initialization with auth data"""
    def test_init_with_auth_data(self):
        api = Booking(ses=some_ses, cookies=some_cookies, account_id=some_account_id)
        ses_value = api.access_ses()
        cookies_value = api.access_cookies()
        account_id_value = api.access_account_id()
        self.basic_assert_auth_data(ses_value, cookies_value, account_id_value)
        self.assertEqual(some_ses, ses_value, f'ses was set to {ses_value}, expected {some_ses}')
        self.assertEqual(some_cookies, cookies_value, f'cookies were set to {cookies_value}, expected {some_cookies}')
        self.assertEqual(some_account_id, account_id_value, f'account_id was set to {account_id_value}, expected {some_account_id}')

class TestBookingInitExceptions(unittest.TestCase):
    """Negative exceptive initialization tests"""
    def test_basic_init_exceptions(self):
        test_cases = [
            {
                "exception": InvalidParameterError,
                "init_kwargs": {},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"email": some_not_registered_email},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"password": some_password},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": AuthenticationError,
                "init_kwargs": {"email": some_not_registered_email, "password": some_password},
                "msg": "Wrong email."
            },
            {
                "exception": AuthenticationError,
                "init_kwargs": {"email": blocked_account_email, "password": some_password},
                "msg": "Account blocked."
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": some_ses, "cookies": some_cookies},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": some_ses, "account_id": some_account_id},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"cookies": some_cookies, "account_id": some_account_id},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses": some_ses, "cookies": some_cookies, "account_id": some_account_id, "OTP": get_OTP_from_input},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"email": some_not_registered_email,
                                "password": some_password,
                                "ses": some_ses, 
                                "cookies": some_cookies, 
                                "account_id": some_account_id},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"email": some_not_registered_email,
                                "password": some_password,
                                "ses": some_ses, 
                                "account_id": some_account_id},
                "msg": "Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR "
                    "ses, cookies and account_id"
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses":'', "cookies": some_cookies, "account_id": some_account_id},
                "msg": "Wrong usage: ses cannot be blank."
            },
            {
                "exception": InvalidParameterError,
                "init_kwargs": {"ses":some_ses, "cookies": some_cookies, "account_id": 0},
                "msg": "Wrong usage: account_id cannot be blank."
            },

        ]

        for case in test_cases:
            with self.subTest(init_kwargs=case["init_kwargs"], exception=case["exception"]):
                self.assertRaisesRegex(case["exception"], case['msg'], Booking, **case["init_kwargs"])

if __name__ == "__main__":
    unittest.main()
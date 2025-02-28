"""Host methods tests"""
import unittest

from booking_host_api.booking import Booking
from booking_host_api.base import AuthenticationError

from .common import BasicBookingTesting, write_private_data_to_file, read_private_data, compare_dicts
from .common import some_ses, some_cookies, some_property_id

class TestBookingMethods(BasicBookingTesting):
    """
        Positive methods test.
        
        Provide json file ("tests/private_data.json" by default, see common.PRIVATE_DATA_FILE_PATH) with 
        valid ses, cookies and account_id and test cases data. See tests/private_data_template.json for 
        structure of a private data file.

        Run test_init_basic or test_init_otp before running tests to write valid ses, 
        cookies and account_id in the private file or put them manually. 
    """
    @classmethod
    def setUpClass(cls):
        cls.read_private_data_to_class('ses', 'cookies', 'account_id')
        cls.api = Booking(ses=cls.ses, cookies=cls.cookies, account_id=cls.account_id)   

    def test_get_account_reservations(self):
        test_cases:list[dict] = read_private_data('get_reservations_cases')

        for case in test_cases: 
            case_num = case.pop('case_num')
            with self.subTest(case_number=case_num):
                expected_number = case.pop('expected_number')
                expected_reservations = case.pop('expected_reservations')
                # following parameters are not passed to get_account_reservations
                del case['property_id']
                del case['only_smart_flex']
                del case['only_corporate_card']
                del case['only_invoice_required']
                reservations = self.api.get_account_reservations(**case)
                write_private_data_to_file(ses=self.api.access_ses(), cookies=self.api.access_cookies(), account_id=self.api.access_account_id())

                received_number = len(reservations)
                self.assertEqual(
                    received_number, 
                    expected_number, 
                    f'Expected {expected_number} reservations and got {received_number}.'
                    )

                for expected_reservation in expected_reservations:
                    for reservation in reservations:
                            if expected_reservation['id'] == reservation['id']:
                                try:
                                    self.assertEqual(
                                        expected_reservation, 
                                        reservation, 
                                        f"Expected reservation {expected_reservations} and got {reservation} for case #{case_num}"
                                        )
                                # assertion is intercepted and differences are printed out
                                except AssertionError as e:
                                    print(f'Case num {case_num}: expected and returned reservation for booking number {expected_reservation['id']} differ:')
                                    compare_dicts(expected_reservation, reservation, 'expected reservation', 'returned reservation')

    def test_get_property_reservations(self):
        test_cases:list[dict] = read_private_data('get_reservations_cases')

        for case in test_cases: 
            case_num = case.pop('case_num')
            with self.subTest(case_number=case_num):
                expected_number = case.pop('expected_number')
                expected_reservations = case.pop('expected_reservations')
                # following parameter is not passed to get_property_reservations
                del case['only_paid_online']
                reservations = self.api.get_property_reservations(**case)
                write_private_data_to_file(ses=self.api.access_ses(), cookies=self.api.access_cookies(), account_id=self.api.access_account_id())

                received_number = len(reservations)
                self.assertEqual(
                    received_number, 
                    expected_number, 
                    f'Expected {expected_number} reservations and got {received_number}.'
                    )

                for expected_reservation in expected_reservations:
                    for reservation in reservations:
                        if expected_reservation['id'] == reservation['id']:
                            try:
                                self.assertEqual(
                                    expected_reservation, 
                                    reservation, 
                                    f"Expected reservation {expected_reservations} and got {reservation} for case #{case_num}"
                                    )
                            # assertion is intercepted and differences are printed out
                            except AssertionError as e:
                                print(f'Case num {case_num}: expected and returned reservation for booking number {expected_reservation['id']} differ:')
                                compare_dicts(expected_reservation, reservation, 'expected reservation', 'returned reservation')

    def test_get_phone(self):
        test_cases:list[dict] = read_private_data('get_phone_cases')

        for case in test_cases:
            case_num = case.pop('case_num')
            with self.subTest(case_number=case_num):
                expected_phone = case.pop('phone')
                phone = self.api.get_phone(**case)
                write_private_data_to_file(ses=self.api.access_ses(), cookies=self.api.access_cookies(), account_id=self.api.access_account_id())

                self.assertEqual(
                    expected_phone, 
                    phone, 
                    f'Expected {expected_phone} for booking number {case['booking_id']} and got {phone}.'
                    )


    def test_get_payout(self):
        test_cases:list[dict] = read_private_data('get_payout_cases')

        for case in test_cases:
            case_num = case.pop('case_num')
            with self.subTest(case_number=case_num):
                expected_payout = case.pop('payout')
                payout = self.api.get_payout(**case)
                write_private_data_to_file(ses=self.api.access_ses(), cookies=self.api.access_cookies(), account_id=self.api.access_account_id())
                
                self.assertEqual(
                    expected_payout, 
                    payout, 
                    f'Expected {expected_payout} for booking number {case['booking_id']} and got {payout}.'
                    )

    def test_get_properties(self):
        expected_properties = read_private_data('expected_properties')
        properties = self.api.get_properties()

        self.assertEqual(
            properties, 
            expected_properties, 
            f'Expected {expected_properties} and got {properties}.'
            )

    def test_get_ics_calendar(self):
        expected_calendar_data:dict = read_private_data('expected_calendar_case')

        property_id = expected_calendar_data.pop('property_id')
        room_id = expected_calendar_data.pop('room_id')

        calendar = self.api.get_ics_calendar(property_id, room_id)
        # most basic assertion is made
        assert calendar, 'Calendar is blank.'

class TestBookingMethodsExceptions(BasicBookingTesting):
    """
        Negative exceptive methods test.
        
        Provide json file ("tests/private_data.json" by default, see common.PRIVATE_DATA_FILE_PATH) with 
        valid ses, cookies and account_id. See tests/private_data_template.json for 
        structure of a private data file.
    """
    @classmethod
    def setUpClass(cls):
        cls.read_private_data_to_class('ses', 'cookies', 'account_id')

    def test_methods_exceptions(self):
        test_cases = [
            {   
                "init_kwargs": {
                    'ses': some_ses, 
                    'cookies': self.cookies, 
                    'account_id': self.account_id,
                    },
                'msg': 'ses or cookies are expired or nonvalid. Update running with an email and password. '
                    'To run get_account_reservations use ses/cookies retrieved with OTP initialization.'
            },
            {   
                "init_kwargs": {
                    'ses': self.ses, 
                    'cookies': some_cookies, 
                    'account_id': self.account_id,
                    },
                'msg': 'ses or cookies are expired or nonvalid. Update running with an email and password. '
                    'To run get_account_reservations use ses/cookies retrieved with OTP initialization.'
            },
        ]
        
        some_date_min = '2024-09-01'
        some_date_max = '2025-02-13'

        for case in test_cases:
            msg = case['msg']
            api = Booking(**case['init_kwargs'])
            with self.subTest(case=case['init_kwargs']):         
                self.assertRaisesRegex(AuthenticationError, msg, api.get_account_reservations, date_min=some_date_min, date_max=some_date_max)

        for case in test_cases:
            msg = case['msg']
            api = Booking(**case['init_kwargs'])
            with self.subTest(case=case['init_kwargs']):
                self.assertRaisesRegex(AuthenticationError, msg, api.get_property_reservations, property_id=some_property_id, date_min=some_date_min, date_max=some_date_max)

if __name__ == "__main__":
    unittest.main()
"""Simple API wrapper for hosts at Booking.com"""

import re
from datetime import datetime, date
from typing import Literal, TypedDict, Callable
from decimal import Decimal, InvalidOperation

import requests
from requests.utils import dict_from_cookiejar
from requests.exceptions import JSONDecodeError

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from .base import BaseScraping, AuthenticationError, InvalidParameterError, ScrapingError
from . import booking_locators as locators
from .config import ELEMENT_WAIT_TIMEOUT, SETUP_WAIT_TIMEOUT, ACCOUNT_RESERVATIONS_ENTRIES_LIMIT, PROPERTY_RESERVATIONS_ENTRIES_LIMIT

def raise_auth_error_or_for_status(response):
    if response.status_code == 401 and response.reason == 'Unauthorized' or \
        response.status_code == 400 and response.reason == 'Bad Request':
        raise AuthenticationError('ses or cookies are expired or nonvalid. Update running with an email and password. '
            'To run get_account_reservations use ses/cookies retrieved with OTP initialization.')
    else:
        response.raise_for_status()

def raise_if_blank(args:dict):
    for arg_name, arg in args.items():
        if not arg:
            raise InvalidParameterError(f'Wrong usage: {arg_name} cannot be blank.')
        
def raise_scraping_error(locators, original_exception, extra_raise_condition = None):
    msg = f'{extra_raise_condition} and none of expected locators: {locators} were not found.' \
        if extra_raise_condition else f'None of expected locators: {locators} were not found.'
    raise ScrapingError(msg) from original_exception

class Reservation(TypedDict):
    id: str
    checkin: date
    checkout: date
    property_id: int
    property_name: str
    rooms: list[dict[str, int|str]]|None    # rooms can be set to None if method doesn't imply it 
    booked_date: date
    guest_name: str
    adults: int
    children: list[int, list[int]]|None     # Number of children if any and their ages in list
    total_price: Decimal    # Can be set to 0.00 by some methods if reservation is cancelled 
    fee: Decimal    # Fee shown on the reservation webpage, not the actual paid fee 
    currency: str
    status: str

    @classmethod
    def normalize(cls, reservation: "Reservation") -> dict[str, str|int|list]:
        """
          - date -> ISO (YYYY-MM-DD)
          - Decimal -> str
        """
        return {
            "id": reservation["id"],
            "checkin": reservation["checkin"].isoformat(),
            "checkout": reservation["checkout"].isoformat(),
            "property_id": reservation["property_id"],
            "property_name": reservation["property_name"],
            "rooms": reservation["rooms"],
            "booked_date": reservation["booked_date"].isoformat(),
            "guest_name": reservation["guest_name"],
            "adults": reservation["adults"],
            "children": reservation["children"],
            "total_price": str(reservation["total_price"]),
            "fee": str(reservation["fee"]),
            "currency": reservation["currency"],
            "status": reservation["status"],
        }

class Booking(BaseScraping):
    """
        Main class providing access to host data.

        Usage

        Initial run with credentials (uses selenium scraping)::

            api = Booking(email='your_email@domain.com', password='your_password')

        Saving auth data::

            ses = api.access_ses()
            cookies = api.access_cookies()
            account_id = api.access_account_id()
            
        Running host methods (uses requests)::

            properties = api.get_properties()
            reservations = api.get_property_reservations(property_id=12345678, date_min='2025-01-01', date_max='2025-02-01')
            phone = api.get_phone(booking_id='4843135716', property_id=12345678)
            payout = api.get_payout(booking_id='4843135716', property_id=12345678)
            calendar = api.get_ics_calendar(booking_id='4843135716', room_id='01')

        Initial run with auth data saved before (initializing runs much faster, no scraping is used)::

            api = Booking(ses=ses, cookies=cookies, account_id=account_id)
            reservations = api.get_property_reservations(property_id=12345678, date_min='2025-01-01', date_max='2025-02-01')
        
        Initializing with auth data (ses, cookies, account_id) saved with credentials only initialization gives access to all methods, 
        except get_account_reservations. To run this one use
        
        Initial run with OTP::

            api = Booking(email='your_email@domain.com', password='your_password', OTP=your_get_OTP_func)

            ses_with_otp = api.access_ses()
            cookies_with_otp = api.access_cookies()
            account_id_with_otp = api.access_account_id()
            
        Initializing with OTP or using corresponding auth data gives access to get_account_reservations, 
        providing reservations for all account properties (also runs faster then get_property_reservations)::
            
            api = Booking(ses=ses_with_otp, cookies=cookies_with_otp, account_id=account_id_with_otp)
            reservations = api.get_account_reservations(date_min='2025-01-01', date_max='2025-02-01')

    """
    
    def __init__(
        self, 
        email:str|None = None,
        password:str|None = None,
        browser_args:list|None = None, 
        page_load_strategy:str|None = 'none',
        ses:str|None = None,
        cookies:dict|None = None,
        account_id:int|None = None,
        OTP:Callable[[str], str]|None = None
        ) -> None:
        """
        Sets auth data (ses, cookies, account_id) for using in host methods.

        Usage options::

            api = Booking(email='your_email@domain.com', password='your_password')
            api = Booking(email='your_email@domain.com', password='your_password', account_id=12345678)
            api = Booking(email='your_email@domain.com', password='your_password', OTP=your_get_OTP_func)
            api = Booking(email='your_email@domain.com', password='your_password', account_id=12345678, OTP=your_get_OTP_func)
        
        Initializing with auth data (ses, cookies, account_id) saved before is fastest method::
            
            api = Booking(ses=ses, cookies=cookies, account_id=account_id)

        Args:
            - email, password: credentials at Booking.com.
            - browser_args, page_load_strategy: selenium session arguments. By default browser_args will be ['--disable-gpu', '--headless']. \
                Pass browser_args=[] to run Selenium defaults.
            - ses, cookies, account_id - auth data saved before
            - OTP function which returns OTP code in string. Function should receive string argument with message.
        """

        # init with nonblank auth data
        if ses is not None and cookies is not None and account_id is not None and email is None and password is None and OTP is None:
            raise_if_blank({'ses': ses, 'cookies': cookies, 'account_id': account_id})
            self._ses = ses
            self._cookies = cookies
            self._account_id = account_id

        # init with nonblank credentials
        elif email is not None and password is not None and ses is None and cookies is None:
            raise_if_blank({'email': email, 'password': password})
            if account_id is not None:
                raise_if_blank({'account_id': account_id})

            self._ses = None
            self._cookies = None
            # account_id is not falsy - correct
            self._account_id = account_id
            self._OTP_func = OTP

            if browser_args is None:
                browser_args = [
                    '--disable-gpu',
                    '--headless'
                ]

            # login and setup auth data (ses, cookies, account_id if needed with Selenium
            super().__init__(
                email=email,
                password=password,
                browser_args=browser_args, 
                page_load_strategy=page_load_strategy,
                )
        # other init options are wrong usage
        else:
            raise InvalidParameterError('Wrong usage: provide nonblank/nonzero values for email, password and optional account_id OR '
                'ses, cookies and account_id')
        
        # checking if attributes are truthy
        if not self._ses:
            raise ScrapingError('Scraping failed: ses value was not set.')
        if not self._cookies:
            raise ScrapingError('Scraping failed: cookies value was not set.')
        if not self._account_id:
            raise ScrapingError('Scraping failed: account_id value was not set.')
        
        # initializing requests session
        self._session = requests.Session()
        self._session.headers = {
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        }
        self._session.cookies.update(self._cookies)
        
    def _email_login(self):
        def setup(driver):
            if not self._ses:
                match = re.search(r"ses=([^&]+)", driver.current_url)
                if match:
                    self._ses = match.group(1)

            if not self._cookies:
                cookies = {}
                for name in locators.auth_cookie_names:
                    cookie = driver.get_cookie(name)
                    if cookie and 'value' in cookie:
                        cookies[name] = cookie['value']
                    else:
                        break

                if len(cookies) == len(locators.auth_cookie_names):
                    self._cookies = cookies

            if not self._account_id:
                match = re.search(r'accountId.*?(\d+)', driver.page_source)
                if match:
                    self._account_id = int(match.group(1))

            if self._ses and self._cookies and self._account_id:
                return True
            
            return False

        def sms_login():
            sms_verification_link.click()

            # using first phone from the list by default and clicking to send OTP
            try:
                wait_for_element.until(EC.element_to_be_clickable(locators.send_OTP_button_xpath)).click()
            except TimeoutException as e:
                raise_scraping_error(locators.send_OTP_button_xpath, e)
            
            msg = '\nOTP verification required. Enter sms code: '

            while True:
                try:
                    send_OTP_result = wait_for_element.until(EC.any_of(
                        EC.presence_of_element_located(locators.OTP_field_id),
                        EC.presence_of_element_located(locators.OTP_error_block_classname)))
                except TimeoutException as e:
                    raise_scraping_error((locators.OTP_field_id, locators.OTP_error_block_classname), e)
                
                # possibly too many OTP input attempts response
                if locators.OTP_error_block_classname[1] in send_OTP_result.get_attribute('class'):
                    raise AuthenticationError(send_OTP_result.text)

                OTP_field = send_OTP_result
                del send_OTP_result

                OTP = self._OTP_func(msg)
                OTP_field.send_keys(OTP)
                
                try:
                    wait_for_element.until(EC.element_to_be_clickable(locators.verify_OTP_button_xpath)).click()
                except TimeoutException as e:
                    raise_scraping_error(locators.verify_OTP_button_xpath, e)

                try:
                    OTP_verify_result = wait_for_setup.until(
                        lambda driver: setup(driver) or EC.presence_of_element_located(locators.invalid_OTP_id)(driver))
                except TimeoutException as e:
                    raise_scraping_error(locators.invalid_OTP_id, e, extra_raise_condition ='Failed to setup during OTP verification')
                
                # setup was successfully run and returned bool type (True)
                if isinstance(OTP_verify_result, bool):
                    return
                
                error_text = OTP_verify_result.text

                # expecting 'Please enter a valid verification code', 'Please enter a verification code' or
                # 'Enter a code with exactly 6 digits' response text if input is non valid
                if 'enter a' in error_text or '6 digits' in error_text:                     
                    OTP_field.send_keys(Keys.CONTROL + "a")
                    OTP_field.send_keys(Keys.DELETE)
                    msg = 'Invalid OTP. Enter valid code: '
                    continue
                
                # possibly valid OTP but session expired response
                raise AuthenticationError(f'{error_text}')

        driver = self.driver
        OTP_required = bool(self._OTP_func)
        login_url = locators.login_otp_url if OTP_required else locators.login_basic_url
        driver.get(login_url)

        wait_for_element = WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT)

        try:
            wait_for_element.until(EC.presence_of_element_located(locators.email_field_id)).send_keys(self._email)
        except TimeoutException as e:
            raise_scraping_error(locators.email_field_id, e)
        
        try:
            wait_for_element.until(EC.element_to_be_clickable(locators.next_button_css)).click()
        except TimeoutException as e:
            raise_scraping_error(locators.next_button_css, e)
        
        try:
            send_email_result = wait_for_element.until(EC.any_of(
                EC.presence_of_element_located(locators.password_field_id), 
                EC.presence_of_element_located(locators.invalid_email_id)
                ))
        except TimeoutException as e:
            raise_scraping_error((locators.password_field_id, locators.invalid_email_id), e)
        
        if send_email_result.get_attribute('id') == locators.invalid_email_id[1]:
            raise AuthenticationError('Wrong email.')
        
        password_field = send_email_result
        del send_email_result

        password_field.send_keys(self._password)

        try:
            wait_for_element.until(EC.element_to_be_clickable(locators.signin_button_css)).click()
        except TimeoutException as e:
            raise_scraping_error(locators.signin_button_css, e)
        
        wait_for_setup = WebDriverWait(driver, SETUP_WAIT_TIMEOUT)

        if not OTP_required:
            try:
                signin_result = wait_for_setup.until(
                    lambda driver: setup(driver) or EC.any_of(
                        EC.presence_of_element_located(locators.invalid_password_id),
                        EC.presence_of_element_located(locators.account_locked_css),
                        EC.presence_of_element_located(locators.sms_verification_link_css)
                    )(driver))
            except TimeoutException as e:
                raise_scraping_error(locators.invalid_password_id, e, extra_raise_condition='Failed to setup')
            
            # setup was successfully run and returned bool type (True)
            if isinstance(signin_result, bool):         
                return
            
            elif signin_result.get_attribute('id') == locators.invalid_password_id[1]:
                raise AuthenticationError('Wrong password.')
            
            elif signin_result.get_attribute('class') == locators.account_locked_css[1]:
                raise AuthenticationError('Account blocked.')
            else:
                raise ScrapingError('Unexpected OTP verification was required. Run with OTP parameter.')
        
        else:
            try:
                signin_result = wait_for_element.until(EC.any_of(
                        EC.presence_of_element_located(locators.invalid_password_id),
                        EC.presence_of_element_located(locators.sms_verification_link_css)
                    ))
            except TimeoutException as e:
                raise_scraping_error((locators.invalid_password_id, locators.sms_verification_link_css), e)

            if signin_result.get_attribute('id') == locators.invalid_password_id[1]:
                raise AuthenticationError('Wrong password.')
            
            sms_verification_link = signin_result
            del signin_result

            # using sms verification by default
            sms_login()

    def _login(self):
        """Logs in and sets up ses, cookies, account_id using Selenium browser"""
        self._email_login()

    def access_ses(self) -> str:
        return self._ses
    
    def access_cookies(self) -> dict:
        return self._cookies
    
    def access_account_id(self) -> int:
        return self._account_id
    
    def _update_cookies(self):
        received_cookies = dict_from_cookiejar(self._session.cookies)
        if received_cookies != self._cookies:
            self._cookies = received_cookies

    def get_properties(self) -> list[dict[str:int|str]]:
        """ 
            Returns list of dictionaries with property id and name in the following format::
        
                {
                'id': 12345678,           #  property id as int
                'name': 'property_name'   #  property name as str
                }
        """
        headers = {
            'referer': 'https://admin.booking.com/hotel/hoteladmin/groups/home/index.html',
        }

        params = {
            'lang': 'xu',
            'ses': self._ses,
        }

        json_data = {
            'operationName': 'propertyListv2',
            'variables': {
                'input': {
                    'accountId': self._account_id,
                    'viewType': 'MULTI_PROPERTY',
                    'pagination': {
                        'offset': 0,         
                        'rowsPerPage': 21,  # possibly no pagination provided in native API
                    },
                },
            },
            'extensions': {},
            'query': 'query propertyListv2($input: PropertyListInput!) {\n  partnerProperty {\n    propertyListv2(input: $input) {\n      currentProperty {\n        id\n        photoUrl\n        propertyPageUrl\n        name\n        __typename\n      }\n      properties {\n        id\n        photoUrl\n        extranetUrl\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
        }
        

        all_properties = []

        response = self._session.post(locators.endpoint_graphql, params=params, headers=headers, json=json_data,)
        raise_auth_error_or_for_status(response)
        self._update_cookies()

        try:
            for entry in response.json()['data']['partnerProperty']['propertyListv2']['properties']:
                all_properties.append({
                    'id': entry['id'],
                    'name': entry['name']
                    })
        except (KeyError, JSONDecodeError) as e:
            raise ValueError('Unexpected response') from e

        return all_properties

    def get_account_reservations(
            self,  
            date_min:str,   # use 'YYYY-MM-DD' format
            date_max:str,   # use 'YYYY-MM-DD' format
            date_of:Literal['reservation', 'check_in', 'check_out'] = 'reservation',           
            show_ok:bool = True,
            show_canceled:bool = True,
            show_no_show:bool = True,
            only_paid_online:bool = True,
            only_pending_request:bool = False,
            keywords:str = '',
            return_normalized = False
            ) -> list[Reservation]:
        """
            Returns list of Reservation dictionaries with booking info for bookings requested in arguments. 
            Returned values - according to Reservation class.

            To use method, instance should be initialized with credentials and OTP or with corresponding 
            auth data (ses, cookies, account_id delivered by an instance which was initialized with credentials and OTP).

            All arguments are used in the same way as interface on group reservations page:
            https://admin.booking.com/hotel/hoteladmin/groups/reservations/index.html 

            Use return_normalized = True to return normalized data where only str, int, list are used in returned values. 
        """
        def process_reservation(entry:dict, properties:list):
            try:
                reservation: Reservation = {
                    "id": entry["id"],
                    "checkin": datetime.strptime(entry["checkin"], "%Y-%m-%d").date(),
                    "checkout": datetime.strptime(entry["checkout"], "%Y-%m-%d").date(),
                    'property_id': entry['propertyId'],
                    "property_name": next(
                        (listing["name"] for listing in properties if listing['id'] == entry['propertyId']), 'Property name was not found'
                        ),
                    "rooms": None, # rooms are not set by this method. Use get_property_reservations to get rooms.
                    "booked_date": datetime.strptime(entry["createdAt"].split()[0], "%Y-%m-%d").date(),             
                    "guest_name": entry["bookerFirstName"] + ' ' + entry["bookerLastName"],
                    "adults": entry["occupancy"]['adults'] if entry["occupancy"]['adults'] is not None else entry["occupancy"]['guests'],
                    "children": [entry["occupancy"]['children'], entry["occupancy"]['childrenAges']]
                        if entry["occupancy"]['children'] else None,
                    "total_price": Decimal(entry["amountInvoicedOrRoomPriceSumRaw"]),
                    'fee': Decimal(entry["actualCommissionRaw"]),
                    'currency': entry['currencyCode'],
                    "status": entry["aggregatedRoomStatus"]
                    }
                
            except (KeyError, ValueError, InvalidOperation, IndexError):
                raise ValueError('Unexpected response.') from e        
                
            return reservation
        
        headers = {
            'referer': 'https://admin.booking.com/hotel/hoteladmin/groups/reservations/index.html',
            'x-booking-context-action': 'groups_reservations_index',
            'x-booking-context-action-name': 'groups_reservations_index',
            }
        
        type_of_date_mapping = {
            'reservation': 'BOOKING', 
            'check_in': 'ARRIVAL', 
            'check_out': 'DEPARTURE'
        }
        type_of_date = type_of_date_mapping[date_of]

        params = {
            'lang': 'en',
            'ses': self._ses,
            'hotel_id': None,       #not needed for this type of request
            'dateType': type_of_date,
            'dateFrom': date_min,
            'dateTo': date_max,
        }
        
        limit = ACCOUNT_RESERVATIONS_ENTRIES_LIMIT 
        json_data = {
            'operationName': 'searchReservations',
            'variables': {
                'paymentStatusFeatureActive': True,
                'input': {
                    'typeOfDate': type_of_date, 
                    'dateFrom': date_min, 
                    'dateTo': date_max, 
                    'searchTerm': keywords,
                    'onlyPendingRequests': only_pending_request,
                    'statusCriteria': {
                        'showCancelled': show_canceled,
                        'showOk': show_ok,
                        'showNoShow': show_no_show,
                        'showPaidOnline': only_paid_online,
                    },
                    'pagination': {
                        'rowsPerPage': limit,
                        'offset': None            # offset will be set in cycle
                    },
                     'accountId': self._account_id
                     
                },
            },
            'extensions': {},
            'query': 'query searchReservations($input: SearchReservationInput!, $paymentStatusFeatureActive: Boolean = false) {\n  partnerReservation {\n    searchReservations(input: $input) {\n      properties {\n        address\n        countryCode\n        cityName\n        extranetHomeUrl\n        status\n        name\n        id\n        __typename\n      }\n      reservations {\n        actualCommissionRaw\n        aggregatedRoomStatus\n        amountInvoicedOrRoomPriceSum\n        amountInvoicedOrRoomPriceSumRaw\n        bookerFirstName\n        bookerLastName\n        createdAt\n        currencyCode\n        propertyId\n        id\n        isGeniusUser\n        checkout\n        checkin\n        occupancy {\n          guests\n          adults\n          children\n          childrenAges\n          __typename\n        }\n        pendingGuestRequestCount\n        paymentStatus @include(if: $paymentStatusFeatureActive)\n        __typename\n      }\n      reservationsHavePaymentCharge\n      totalRecords\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        total_count = None
        offset = 0
        properties = None
        all_reservations = []

        try:
            while total_count is None or offset < total_count:
                json_data['variables']['input']['pagination']['offset'] = offset

                response = self._session.post(locators.endpoint_graphql, headers=headers, params=params, json=json_data)
                raise_auth_error_or_for_status(response)
                self._update_cookies()
                response_json = response.json()

                if properties is None:
                    properties = response_json['data']['partnerReservation']['searchReservations']['properties']
                for entry in response_json['data']['partnerReservation']['searchReservations']['reservations']:
                    reservation = process_reservation(entry=entry, properties=properties)
                    all_reservations.append(reservation)

                if total_count is None:
                    total_count = response_json['data']['partnerReservation']['searchReservations']['totalRecords']
                offset += limit
        except (KeyError, JSONDecodeError) as e:
            raise ValueError('Unexpected response.') from e

        if return_normalized:
            all_reservations_normalized = [Reservation.normalize(reservation) for reservation in all_reservations]
            return all_reservations_normalized
        else:
            return all_reservations 

    def get_property_reservations(
            self,
            property_id:int,
            date_min:str,       # use 'YYYY-MM-DD' format
            date_max:str,       # use 'YYYY-MM-DD' format
            date_of:Literal['reservation', 'check_in', 'check_out', 'invoice', 'stay'] = 'reservation',           
            show_ok:bool = True,
            show_canceled:bool = True,
            show_no_show:bool = True,
            only_smart_flex:bool = False,
            only_corporate_card:bool = False,
            only_pending_request:bool = False,
            only_invoice_required:bool = False,
            keywords:str = '',
            return_normalized = False
            ) ->list[Reservation]:
        """
            Returns list Reservation dictionaries with booking info for bookings requested in arguments.
            Returned values - according to Reservation class.

            All arguments are used in the same way as interface on property reservations page:
            https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/search_reservations.html?source=nav&upcoming_reservations=1&hotel_id=...

            Use return_normalized = True to return normalized data where only str, int, list are used in returned values. 
        """
        
        def process_reservation(entry:dict, property_id:int, property_name:str) -> dict:
            try:
                reservation: Reservation = {
                    "id": str(entry["id"]),
                    "checkin": datetime.strptime(entry["checkin"], "%Y-%m-%d").date(),
                    "checkout": datetime.strptime(entry["checkout"], "%Y-%m-%d").date(),
                    'property_id': property_id,
                    "property_name": property_name,
                    "rooms": entry["rooms"],
                    "booked_date": datetime.strptime(entry["bookDate"], "%Y-%m-%d").date(),             
                    "guest_name": entry["guestName"],
                    "adults": entry["occupancy"].get('adults', entry["occupancy"].get('guests', None)),
                    "children": [entry["occupancy"].get('children', None), list(map(int, entry["occupancy"].get('childrenAges', None) or []))]
                        if entry["occupancy"].get('children', None) else None,
                    "total_price": Decimal(entry["price"]["formatted"].split('; ')[1]).quantize(Decimal("0.00")),
                    'fee': Decimal(entry["commission"]["original"]["formatted"].split('; ')[1]).quantize(Decimal("0.00")),
                    'currency': entry['price']["currency"],
                    "status": entry["reservationStatus"]
                    }
                
            except (KeyError, ValueError, InvalidOperation, IndexError) as e:
                raise ValueError('Unexpected response.') from e        
                
            return reservation

        headers = {
            'referer': 'https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/search_reservations.html'
        }

        type_of_date_mapping= {
            'reservation': 'booking', 
            'check_in': 'arrival', 
            'check_out': 'departure', 
            'invoice': 'invoiced', 
            'stay': 'stay'
        }
        type_of_date = type_of_date_mapping[date_of]
        limit = PROPERTY_RESERVATIONS_ENTRIES_LIMIT
        user_reservation_options = [
            (show_ok, "ok"),
            (show_canceled, "cancelled"),
            (show_no_show, "no_show"),
            (only_smart_flex, "risk_free"),
            (only_corporate_card, "paid_with_corporate_vcc")
        ]
        reservation_status = [label for flag, label in user_reservation_options if flag]

        params = {
            'hotel_id': property_id,
            'ses': self._ses,
            'hotel_account_id': self._account_id,
            'lang': 'en',
            'perpage': limit,
            'page': None,               # page will be set in cycle
            'date_type': type_of_date,
            'date_from': date_min,
            'date_to': date_max,
            'display_filters': 'true',
            'reservation_status[]': reservation_status,
            'term': keywords,
            'token': 'empty-token',
            'user_triggered_search': '1'
        }
        if only_invoice_required:
            params['invoice_required[]'] = ['required']
        if only_pending_request:
            params['pending_request[]'] = ['pending']

        all_reservations = []
        page_num = 1
        has_next_page = True
        all_properties = self.get_properties()

        try:
            while has_next_page:            # has_next_page strategy should be revised
                params['page'] = page_num   
                response = self._session.post(url=locators.endpoint_property_reservations, headers=headers, params=params)
                raise_auth_error_or_for_status(response)
                self._update_cookies()
                response_json = response.json()
                property_id_from_response = int(response_json['params']['details']['hotel_id']['value'])
                property_name = next((listing['name'] for listing in all_properties if listing['id'] == property_id_from_response))
                for entry in response_json['data']['reservations']:
                    reservation = process_reservation(entry, property_id_from_response, property_name)
                    all_reservations.append(reservation)
            
                has_next_page = response_json['data']['hasNextPage']
                page_num += 1

        except (KeyError, ValueError, JSONDecodeError, StopIteration) as e:
            raise ValueError('Unexpected response.') from e

        if return_normalized:
            all_reservations_normalized = [Reservation.normalize(reservation) for reservation in all_reservations]
            return all_reservations_normalized
        
        return all_reservations

    def get_phone(self, booking_id:str, property_id:int) -> str:
        """
            Returns phone in string form for booking number and property id specified.

            If seeing guest phone availability is expired, will return 'Expired'.
        """
        params = {
            'hotelreservation_id' : booking_id,
            'hotel_account_id': self._account_id,
            'lang': 'xu',
            'ses': self._ses,
            'hotel_id': property_id,
        }

        response = self._session.get(url=locators.endpoint_guest_profile, params=params)
        raise_auth_error_or_for_status(response)
        self._update_cookies()
        try:
            response_json = response.json()['data']
            if not response_json['booker_profile_expired']:
                raw_phone = response_json['phone_number']
                return re.sub(r'\s+', '', raw_phone)
            else: 
                return 'Expired'
        except (KeyError, TypeError, JSONDecodeError)  as e:
            raise ValueError('Unexpected response') from e

    def get_payout(self, booking_id:str, property_id:int, return_normalized:bool=False) -> Decimal|str:
        """
            Returns actual paid payout for booking number and property id.

            'Pending' is returned if not paid.
            
            Use return_normalized = True for return in str.
        """
        params = {
            'hres_id': booking_id,
            'hotel_account_id': self._account_id,
            'hotel_id': property_id,
            'lang': 'xu',
            'ses': self._ses
        }
        response = self._session.post(url=locators.endpoint_payout, params=params)
        raise_auth_error_or_for_status(response)
        self._update_cookies()

        try:
            response_json = response.json()['data']
            raw_payout = response_json['amountToTransfer']
            if raw_payout is None:
                    payout = Decimal('0.00')
            else:
                payout_status = response_json['payoutStatus']
                if payout_status == 'pending':
                        return 'Pending'
                elif payout_status == 'paid':
                    payout = Decimal(re.sub(r'[^0-9.]', '', raw_payout))
                else: 
                    raise ValueError
        except (KeyError, ValueError, UnboundLocalError, InvalidOperation, JSONDecodeError)  as e:
            raise ValueError('Unexpected response') from e
        
        return str(payout) if return_normalized else payout
        
    def get_ics_calendar(self, property_id:int, room_id:str) -> str:
        """
            Returns ics format calendar in string for property and room ids.

            room_id should be string containing 2 digits: '01', '12' etc.
        """
        headers = {
            'referer': 'https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/sync/index.html',
        }
    
        params = {
            'hotel_id': property_id,
            'ses': self._ses,
            'hotel_account_id': self._account_id,
            'lang': 'en',
            'room_id': str(property_id)+room_id,
            'name': 'random_name_for_response',
        }

        response = self._session.post(url=locators.endpoint_calendar_export, headers=headers, params=params)
        raise_auth_error_or_for_status(response)
        self._update_cookies()

        try:
            calendar_url = response.json()['data']['url']
        except (KeyError, JSONDecodeError) as e:
            raise ValueError('Unexpected response') from e
        
        calendar = self._session.get(url=calendar_url)
        raise_auth_error_or_for_status(calendar)
        normalized_text = calendar.text.replace('\r\n', '\n')
        return normalized_text
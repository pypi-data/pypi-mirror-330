# Booking.com API wrapper for hosts

## Disclaimer
This is an unofficial python API wrapper for hosts at booking.com. Provides access with email and 
password to host reservations, properties, calendar and other data.

Using this software might contradict booking.com terms of service. Use in educational purpose only.

## Requirements
- selenium
- requests
- filelock for tests

To install requirements:
pip install -r requirements.txt

## Install
pip install booking-host-api

## Usage

```
from booking_host_api import Booking
```

### Initial run with credentials (uses selenium scraping)

```
api = Booking(email='your_email@domain.com', password='your_password')
```

### Saving auth data

```
ses = api.access_ses()
cookies = api.access_cookies()
account_id = api.access_account_id()
```

### Running host methods (uses requests)

```
properties = api.get_properties()
reservations = api.get_property_reservations(property_id=12345678, date_min='2025-01-01', date_max='2025-02-01')
phone = api.get_phone(booking_id='1234567890', property_id=12345678)
payout = api.get_payout(booking_id='1234567890', property_id=12345678)
calendar = api.get_ics_calendar(booking_id='1234567890', room_id='01')
```

### Initial run with auth data saved before (initializing runs much faster, no scraping is used)

```
api = Booking(ses=ses, cookies=cookies, account_id=account_id)
reservations = api.get_property_reservations(property_id=12345678, date_min='2025-01-01', date_max='2025-02-01')
```

Initializing with auth data (ses, cookies, account_id), saved with credentials only initialization, gives access to all methods, 
except get_account_reservations. To run this one use

### Initial run with OTP

```
api = Booking(email='your_email@domain.com', password='your_password', OTP=your_get_OTP_func)

ses_with_otp = api.access_ses()
cookies_with_otp = api.access_cookies()
account_id_with_otp = api.access_account_id()
```

Initializing with OTP or using corresponding auth data gives access to get_account_reservations, 
providing reservations for all account properties (also runs faster then get_property_reservations)::

```
api = Booking(ses=ses_with_otp, cookies=cookies_with_otp, account_id=account_id_with_otp)
reservations = api.get_account_reservations(date_min='2025-01-01', date_max='2025-02-01')
```

### Testing
Provide json file ("tests/private_data.json" by default, see common.PRIVATE_DATA_FILE_PATH) with valid testing data.
See tests/private_data_template.json for structure of a private data file.

Example of running one test method:

py -m unittest tests.test_booking_init.TestBookingCredentialsInit.test_init_otp


Running all test (be sure to put in advance all necessary data in private_data.json file):

python -m unittest discover
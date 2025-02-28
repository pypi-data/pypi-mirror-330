from selenium.webdriver.common.by import By

login_basic_url = 'https://admin.booking.com/'
login_otp_url = 'https://admin.booking.com/hotel/hoteladmin/groups/reservations/index.html'

email_field_id = (By.ID, "loginname")
next_button_css = (By.CSS_SELECTOR, "button[data-dv-event-id='1']")
invalid_email_id = (By.ID, 'loginname-note')
password_field_id = (By.ID, "password")
invalid_password_id = (By.ID, 'password-note')
account_locked_css = (By.CLASS_NAME, "nw-account-locked")
signin_button_css = (By.CSS_SELECTOR, "button[data-dv-event-id='10']")

sms_verification_link_css = (By.CSS_SELECTOR, "a.nw-sms-verification-link")
send_OTP_button_xpath =(By.XPATH, "//button[.//span[contains(text(), 'Send')]]")
OTP_field_id = (By.ID, "sms_code")
verify_OTP_button_xpath = (By.XPATH, "//button[.//span[contains(text(),'Verify')]]")
invalid_OTP_id = (By.ID, 'sms_code-note')
OTP_error_block_classname = (By.CLASS_NAME, "error-block")

auth_cookie_names = [
    'esadm',
    'ecid'
]

endpoint_graphql = 'https://admin.booking.com/dml/graphql.json'
endpoint_property_reservations = 'https://admin.booking.com/fresa/extranet/reservations/retrieve_list_v2'
endpoint_guest_profile = 'https://admin.booking.com/fresa/booker_profile/retrieve'
endpoint_payout = 'https://admin.booking.com/fresa/extranet/reservations/details/get_reservation_payout'
endpoint_calendar_export = 'https://admin.booking.com/fresa/extranet/ical/create_export_link'

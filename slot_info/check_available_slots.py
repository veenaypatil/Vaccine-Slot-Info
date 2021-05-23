import time
from datetime import datetime

import click
import requests

from slot_info.cowin_api import *
from slot_info.session_requests import SessionRequest
from slot_info.telegram import send_telegram_message
from slot_info.whatsapp import send_whatsapp_message
from cacheout import Cache
from slot_info.constants import vaccine_types, dose_numbers

# cache ttl is of 1 minute, this is to avoid sending multiple notifications
cache = Cache(ttl=600)
session_requests = SessionRequest()


@click.group()
def main():
    """
    CLI for checking the Appointments in your District.
    """
    pass


@main.command(name="pincode-wise")
@click.option("-pin", "--pin_code",
              type=str,
              required=True,
              help="Pin code of your area to search for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def pincode_wise(pin_code, date, age_filter, notify_on, vaccine_type, dose_number):
    """
    get pin code wise available slots on a specific date in a given pin.
    """
    print("Checking for available slots in pin code " + str(pin_code) + ", for date " + str(date) +
          ",for min_age: " + str(age_filter))
    check_pincode_wise_slots(pin_code, date, age_filter, notify_on, vaccine_type, dose_number)


@main.command(name="district-wise")
@click.option("-dId", "--district_id",
              type=str,
              required=True,
              help="ID of the district, if you do no know the district ID run get-district-id command")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def district_wise(district_id, date, age_filter, notify_on, vaccine_type, dose_number):
    """
    get district wise available slots on a specific date in a given district.
    """
    print("Checking for available slots in district " + str(district_id) + ", for date " + str(
        date) + ",for min_age: " + str(age_filter))
    check_district_wise_slots(district_id, date, age_filter, notify_on, vaccine_type, dose_number)


@main.command(name="get-state-id")
@click.option("-sn", "--state_name",
              type=str,
              required=True,
              help="Name of the state for which ID is to be retrieved")
def get_state_id(state_name):
    """
    Get's the ID of the state name
    """
    url = BASE_API + get_all_states
    try:
        response_data = session_requests.get(url)
        states = response_data['states']
        state_id = None
        for state in states:
            if state_name == state['state_name']:
                state_id = state['state_id']
                break
        if state_id is None:
            print("Provide proper name of the state")
        else:
            print("State ID is : ", state_id)
    except requests.HTTPError as http_error:
        print_error_message(http_error)


@main.command(name="get-district-id")
@click.option("-sId", "--state_id",
              type=str,
              required=True,
              help="ID of the state, if you do not know the state ID run get-state-id command")
@click.option("-dn", "--district_name",
              type=str,
              required=True,
              help="Name of the district for which ID is to be retrieved")
def get_district_id(state_id, district_name):
    """
    Get's the ID of the district name
    """
    url = BASE_API + get_all_districts.format(state_id)
    try:
        response_data = session_requests.get(url)
        districts = response_data['districts']
        district_id = None
        for district in districts:
            if district_name == district['district_name']:
                district_id = district['district_id']
                break
        if district_id is None:
            print("Provide proper name of the district")
        else:
            print("District ID is : ", district_id)
    except requests.HTTPError as http_error:
        print_error_message(http_error)


@main.command(name="continuously-for-district")
@click.option("-dId", "--district_id",
              type=str,
              required=True,
              help="Provide district Id to check for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-i", "--interval",
              type=int,
              required=True,
              help="Interval in seconds")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def continuously_for_district(district_id, date, age_filter, interval, notify_on, vaccine_type, dose_number):
    """
    Continuously check for available slots in district for a specific date after every x interval seconds
    and notify on whatsapp/telegram
    """
    print("Checking for available slots in district " + str(district_id) + ", for date " + str(
        date) + ",for min_age: " + str(age_filter))
    while True:
        check_district_wise_slots(district_id, date, age_filter, notify_on, vaccine_type, dose_number)
        time.sleep(interval)


@main.command(name="continuously-for-district-next7days")
@click.option("-dId", "--district_id",
              type=str,
              required=True,
              help="Provide district Id to check for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked for next 7 days")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-i", "--interval",
              type=int,
              required=True,
              help="Interval in seconds")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def continuously_for_district_next7days(district_id, date, age_filter, interval, notify_on, vaccine_type, dose_number):
    """
    Continuously check for available slots in district for next 7 days after every x interval seconds
    and notify on whatsapp/telegram
    """
    print("Checking for available slots in district " + str(district_id) + ", for next 7 days starting from date:  "
          + str(date) + ",for min_age: " + str(age_filter))
    while True:
        check_district_wise_slots_next7days(district_id, date, age_filter, notify_on, vaccine_type, dose_number)
        time.sleep(interval)


@main.command(name="continuously-for-pincode")
@click.option("-pin", "--pin_code",
              type=str,
              required=True,
              help="Pin code of your area to search for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-i", "--interval",
              type=int,
              required=True,
              help="Interval in seconds to check for available slots")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def continuously_for_pincode(pin_code, date, age_filter, interval, notify_on, vaccine_type, dose_number):
    """
    Continuously check for available slots in pin code for a specific date after every x interval seconds
    and notify on whatsapp/telegram
    """
    print("Checking for available slots in pin code " + str(pin_code) + ", for date " + str(date) +
          ",for min_age: " + str(age_filter))
    while True:
        check_pincode_wise_slots(pin_code, date, age_filter, notify_on, vaccine_type, dose_number)
        time.sleep(interval)


@main.command(name="continuously-for-pincode-next7days")
@click.option("-pin", "--pin_code",
              type=str,
              required=True,
              help="Pin code of your area to search for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked for next 7 days")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-i", "--interval",
              type=int,
              required=True,
              help="Interval in seconds to check for available slots")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine_type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def continuously_for_pincode_next7days(pin_code, date, age_filter, interval, notify_on, vaccine_type, dose_number):
    """
    Continuously check for available slots in pin code for next 7 days after every x interval seconds
    and notify on whatsapp/telegram
    """
    print("Checking for available slots in pin code " + str(pin_code) + ", for next 7 days starting from date " + str(
        date) + ",for min_age: " + str(age_filter))
    while True:
        check_pincode_wise_slots_next7days(pin_code, date, age_filter, notify_on, vaccine_type, dose_number)
        time.sleep(interval)


@main.command(name="pincode-wise-next7days")
@click.option("-pin", "--pin_code",
              type=str,
              required=True,
              help="Pin code of your area to search for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked for next 7 days")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def pincode_wise_next7days(pin_code, date, age_filter, notify_on, vaccine_type, dose_number):
    """
    Check for available slots in pin code for next 7 days from the date provided
    """
    print("Checking for available slots in pin code " + str(pin_code) + ", for next 7 days starting from date "
          + str(date) + ",for min_age: " + str(age_filter))
    check_pincode_wise_slots_next7days(pin_code, date, age_filter, notify_on, vaccine_type, dose_number)


@main.command(name="district-wise-next7days")
@click.option("-dId", "--district_id",
              type=str,
              required=True,
              help="ID of the district, if you do no know the district ID run get-district-id command")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked for next 7 days")
@click.option("-af", "--age_filter",
              type=int,
              default=18,
              help="Filter only 18 plus or 45 plus appointments")
@click.option("-n", "--notify_on",
              type=click.Choice(['whatsapp', 'telegram']),
              required=True,
              help="Receive notification on whatsapp/telegram")
@click.option("-vt", "--vaccine_type",
              type=click.Choice(vaccine_types, case_sensitive=False),
              required=False,
              multiple=True,
              default=[],
              help="Vaccine type for which appointments are to be checked")
@click.option("-dn", "--dose_number",
              type=click.Choice(dose_numbers),
              required=False,
              multiple=True,
              default=[],
              help="Dose number for which appointments are to be checked")
def district_wise_next7days(district_id, date, age_filter, notify_on, vaccine_type, dose_number):
    """
    Check for available slots in district for next 7 days from the date provided
    """
    print("Checking for available slots in district " + str(district_id) + ", for next 7 days starting from date "
          + str(date) + ",for min_age: " + str(age_filter))
    check_district_wise_slots_next7days(district_id, date, age_filter, notify_on, vaccine_type, dose_number)


def check_pincode_wise_slots(pin_code, date, age_filter, notify_on, vaccine_types, dose_number):
    validate_inputs(date, age_filter)
    url = BASE_API + find_by_pin
    params = {
        "pincode": pin_code,
        "date": date
    }
    try:
        response_data = session_requests.get(url=url, params=params)
        if len(response_data['sessions']) > 0:
            create_message_from_session(response_data['sessions'], age_filter, notify_on, vaccine_types, dose_number)
        else:
            print("No slots are available for pincode: ", pin_code)
    except requests.HTTPError as http_error:
        print_error_message(http_error)


def check_pincode_wise_slots_next7days(pin_code, date, age_filter, notify_on, vaccine_types, dose_number):
    validate_inputs(date, age_filter)
    url = BASE_API + calendar_by_pin

    params = {
        "pincode": pin_code,
        "date": date
    }
    try:
        response_data = session_requests.get(url=url, params=params)
        if len(response_data['centers']) > 0:
            for center in response_data['centers']:
                for session in center['sessions']:
                    session['pincode'] = center['pincode']
                    session['name'] = center['name']
                    sessions = [session]
                    create_message_from_session(sessions, age_filter, notify_on, vaccine_types, dose_number)
        else:
            print("There are no centers available for this pin code")
    except requests.HTTPError as http_error:
        print_error_message(http_error)


def check_district_wise_slots(district_id, date, age_filter, notify_on, vaccine_types, dose_number):
    validate_inputs(date, age_filter)
    url = BASE_API + find_by_district
    params = {
        "district_id": district_id,
        "date": date
    }

    try:
        response_data = session_requests.get(url=url, params=params)
        if len(response_data['sessions']) > 0:
            create_message_from_session(response_data['sessions'], age_filter, notify_on, vaccine_types, dose_number)
        else:
            print("No slots are available for district: ", district_id)
    except requests.HTTPError as http_error:
        print_error_message(http_error)


def check_district_wise_slots_next7days(district_id, date, age_filter, notify_on, vaccine_types, dose_number):
    validate_inputs(date, age_filter)
    url = BASE_API + calendar_by_district
    params = {
        "district_id": district_id,
        "date": date
    }

    try:
        response_data = session_requests.get(url=url, params=params)
        if len(response_data['centers']) > 0:
            for center in response_data['centers']:
                for session in center['sessions']:
                    session['pincode'] = center['pincode']
                    session['name'] = center['name']
                    sessions = [session]
                    create_message_from_session(sessions, age_filter, notify_on, vaccine_types, dose_number)
        else:
            print("There are no centers available for this district")
    except requests.HTTPError as http_error:
        print_error_message(http_error)


def is_slot_available(session, dose_number):
    is_available = False
    if session['available_capacity'] > 0:
        if not dose_number or \
                ("1" in dose_number and session['available_capacity_dose1'] > 0) or \
                ("2" in dose_number and session['available_capacity_dose2'] > 0):
            is_available = True
    return is_available


def create_message_from_session(sessions, age_filter, notify_on, vaccine_types, dose_number):
    message = "Following Centers are available \n\n"
    for session in sessions:
        if is_slot_available(session, dose_number) and \
                session['min_age_limit'] == age_filter and \
                (not vaccine_types or session['vaccine'].lower() in vaccine_types):
            print("Name: " + str(session['name']) + ", PinCode: " + str(session['pincode']) + ", Available: " + str(
                session['available_capacity']) + ", Date :" + str(session['date']))
            if cache.get(str(session['pincode']) + session['name'] + str(session['date'])) is None:
                cache.set(str(session['pincode']) + session['name'] + str(session['date']), 1)
                message = message + "Name : " + str(session['name']) + "\n"
                message = message + "Pincode: " + str(session['pincode']) + "\n"
                message = message + "Vaccine Type: " + str(session['vaccine']) + "\n"
                message = message + "Total Available Capacity: " + str(session['available_capacity']) + "\n"
                if "1" in dose_number and session['available_capacity_dose1'] > 0:
                    message = message + "Available Capacity Dose1: " + str(session['available_capacity_dose1']) + "\n"
                if "2" in dose_number and session['available_capacity_dose2'] > 0:
                    message = message + "Available Capacity Dose2: " + str(session['available_capacity_dose2']) + "\n"
                message = message + "Min Age: " + str(session['min_age_limit']) + "\n"
                message = message + "Date: " + str(session['date']) + "\n"
                send_message(message, notify_on)
                message = "\n\n"
    return message


def send_message(message, notify_on):
    if notify_on == "whatsapp":
        send_whatsapp_message(message)
    elif notify_on == "telegram":
        send_telegram_message(message)


def validate_inputs(date, age_filter):
    if age_filter != 18 and age_filter != 45:
        raise ValueError("Possible values for age_filter is 18 or 45")
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Date should be provided in DD-MM-YYYY format, for example: 10-05-2021")


def print_error_message(http_error):
    error_message = {
        'status_code': http_error.response.status_code,
        'content': http_error.response.content
    }
    print(error_message)


if __name__ == '__main__':
    main()

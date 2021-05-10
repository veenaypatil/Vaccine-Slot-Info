import time
import click
import requests
from slot_info.cowin_api import *
from slot_info.whatsapp import send_whatsapp_message
from cacheout import Cache

# cache ttl is of 1 minute, this is to avoid sending multiple notifications
cache = Cache(ttl=60)


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
def pincode_wise(pin_code, date, age_filter):
    url = BASE_API + find_by_pin
    params = {
        "pincode": pin_code,
        "date": date
    }
    headers = {
        "accept": "application/json",
        "Accept-Language": "hi_IN",
        "user-agent": "*"
    }
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        if len(response_data['sessions']) > 0:
            message = create_message_from_session(response_data['sessions'], age_filter)
            send_whatsapp_message(message)
        else:
            print("No slots are available for pincode: ", pin_code)
    except requests.HTTPError as e:
        print_error_message(e)


def check_district_wise_slots(district_id, date, age_filter):
    if age_filter == 18 or age_filter == 45:
        print("Checking for available slots in district " + str(district_id) + ", for date " + str(
            date) + ",for min_age: " + str(age_filter))
        url = BASE_API + find_by_district
        params = {
            "district_id": district_id,
            "date": date
        }
        headers = {
            "accept": "application/json",
            "Accept-Language": "hi_IN",
            "user-agent": "*"
        }
        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            response_data = response.json()
            if len(response_data['sessions']) > 0:
                message = create_message_from_session(response_data['sessions'], age_filter)
            else:
                print("No slots are available for district: ", district_id)
        except requests.HTTPError as e:
            print_error_message(e)
    else:
        raise ValueError("Possible values for age_filter is 18 or 45")


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
def district_wise(district_id, date, age_filter):
    check_district_wise_slots(district_id, date, age_filter)


def create_message_from_session(sessions, age_filter):
    message = "Following Centers are available \n\n"
    for session in sessions:
        if session['available_capacity'] > 0 and session['min_age_limit'] == age_filter:
            print(str(session['pincode']) + "," + str(session['available_capacity']))
            if cache.get(session['pincode']) is None:
                cache.set(session['pincode'], 1)
                message = message + "Name : " + str(session['name']) + "\n"
                message = message + "Pincode: " + str(session['pincode']) + "\n"
                message = message + "Vaccine Type: " + str(session['vaccine']) + "\n"
                message = message + "Available Capacity: " + str(session['available_capacity']) + "\n"
                message = message + "Min Age: " + str(session['min_age_limit']) + "\n"
                send_whatsapp_message(message)
                message = "\n\n"
    return message


def print_error_message(http_error):
    error_message = {
        'status_code': http_error.response.status_code,
        'content': http_error.response.content
    }
    print(error_message)


@main.command(name="get-state-id")
@click.option("-sn", "--state_name",
              type=str,
              required=True,
              help="Get's the ID of the state name provided")
def get_state_id(state_name):
    url = BASE_API + get_all_states
    headers = {
        "accept": "application/json",
        "Accept-Language": "hi_IN",
        "user-agent": "*"
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
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
    except requests.HTTPError as e:
        print_error_message(e)


@main.command(name="get-district-id")
@click.option("-sId", "--state_id",
              type=str,
              required=True,
              help="ID of the state, if you do no know the state ID run get-state-id command")
@click.option("-dn", "--district_name",
              type=str,
              required=True,
              help="Name of the district for which ID is to be retrieved")
def get_district_id(state_id, district_name):
    url = BASE_API + get_all_districts.format(state_id)
    headers = {
        "accept": "application/json",
        "Accept-Language": "hi_IN",
        "user-agent": "*"
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
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
    except requests.HTTPError as e:
        print_error_message(e)


@main.command()
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
def continuously(district_id, date, age_filter, interval):
    while True:
        check_district_wise_slots(district_id, date, age_filter)
        time.sleep(interval)


if __name__ == '__main__':
    main()

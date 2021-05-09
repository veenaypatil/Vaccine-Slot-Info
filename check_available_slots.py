import time
import click
import requests
from cowin_api import *
from whatsapp import send_whatsapp_message

@click.group()
def main():
    """
    CLI for checking the Appointments in your District.
    """
    pass


@main.command()
@click.option("-pin", "--pin_code",
              type=str,
              required=True,
              help="Pin code of your area to search for appointments")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked")
def pincode_wise(pin_code, date):
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
            message = create_message_from_session(response_data['sessions'])
            send_whatsapp_message(message)
    except requests.HTTPError as e:
        print_error_message(e)


def check_district_wise_slots(district_id, date):
    print("Checking for available slots in district " + str(district_id) + ", for date " + str(date))
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
        print(response_data)
        if len(response_data['sessions']) > 0:
            message = create_message_from_session(response_data['sessions'])
    except requests.HTTPError as e:
        print_error_message(e)


@main.command()
@click.option("-dId", "--district_id",
              type=str,
              required=True,
              help="ID of the district, if you do no know the district ID run get-district-id command")
@click.option("-d", "--date",
              type=str,
              required=True,
              help="Date for which appointments are to be checked")
def district_wise(district_id, date):
    check_district_wise_slots(district_id, date)


def create_message_from_session(sessions):
    message = "Following Centers are available \n\n"
    for session in sessions:
        if session['available_capacity'] > 0:
            message = message + "Name : " + str(session['name']) + "\n"
            message = message + "Pincode: " + str(session['pincode']) + "\n"
            message = message + "Vaccine Type: " + str(session['vaccine']) + "\n"
            message = message + "Slots: " + str(session['slots']) + "\n"
            send_whatsapp_message(message)
            message = "\n\n"
    return message


def print_error_message(http_error):
    error_message = {
        'status_code': http_error.response.status_code,
        'content': http_error.response.content
    }
    print(error_message)


@main.command()
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


@main.command()
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
def continuously(district_id, date):
    while True:
        check_district_wise_slots(district_id, date)
        time.sleep(60)


if __name__ == '__main__':
    main()

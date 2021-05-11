import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_whatsapp_message(message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_mobile_number = os.getenv('FROM_MOBILE_NUMBER')
    to_mobile_number = os.getenv('TO_MOBILE_NUMBER')

    if account_sid is None or auth_token is None:
        raise ValueError("Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN as env variables")

    if from_mobile_number is None or to_mobile_number is None:
        raise ValueError("Please set FROM_MOBILE_NUMBER and TO_MOBILE_NUMBER as env variables")

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        from_='whatsapp:{0}'.format(from_mobile_number),
        body=message,
        to='whatsapp:{0}'.format(to_mobile_number))
    print(message.sid)

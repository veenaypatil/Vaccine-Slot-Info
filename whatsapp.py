import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_whatsapp_message(message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_mobile_number = os.environ['FROM_MOBILE_NUMBER']
    to_mobile_number = os.environ['TO_MOBILE_NUMBER']

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        from_='whatsapp:{0}'.format(from_mobile_number),
        body=message,
        to='whatsapp:{0}'.format(to_mobile_number))
    print(message.sid)

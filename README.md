# Vaccine-Slot-Info
CLI to check for Covid appointments pincode or district wise and get notified on WhatsApp.
This is integrated with Twilio API to send notification to whatsapp.

### Pre-requisites
1. Python 3.6+
2. Twilio Free Trail Account for whatsapp notification

### Twilio
1. Create a new Twilio Trail Account - www.twilio.com/referral/PfBNJy 
2. Export the following env variables
```
export TWILIO_ACCOUNT_SID="twilio_account_sid" // you will get this here https://www.twilio.com/console
export TWILIO_AUTH_TOKEN="twilio_auth_token" // you will get this here https://www.twilio.com/console
export FROM_MOBILE_NUMBER="twilio_number" // you will get this number after following the steps https://www.twilio.com/console/sms/whatsapp/sandbox
export TO_MOBILE_NUMBER="your_mobile_number"
```

### Installation steps to use `slotinfo` command

```
python setup.py sdist
sudo pip install dist/slotinfo-1.0.tar.gz
```

### CLI commands provided by this utility
```
  get-state-id
  get-district-id
  district-wise  
  pincode-wise
  continuously
```

### CLI commands usage
```
1. Get the State ID
slotinfo get-state-id --state_name Maharashtra

2. Get the District ID
slotinfo get-district-id --state_id 21 --district_name Nanded

3. Check available appointment slots district wise
slotinfo district-wise --district_id 334 -date 10-05-2021

4. Check available appointment slots pincode wise
slotinfo pincode-wise -pin 411015 --date 10-05-2021

5. Run the script continously to check for available appointments after evey x(seconds) interval
slotinfo continuously --district_id 363 --date 10-05-2021 --age_filter 18 --interval 2
```

Notification will be send on the whatsapp

<img width="350" alt="Screenshot 2021-05-09 at 10 01 03 PM" src="https://user-images.githubusercontent.com/52563354/117579869-927b1680-b112-11eb-9403-21438d53bc46.png">


### TODO
[] Add SMS, Email notification

# Vaccine-Slot-Info
CLI to continuously check for appointments and get notified on WhatsApp

This is integrated with Twilio API to send notification to whatsapp. Currently only a Trail account is used of Twilio.

### Twilio
1. Create a new Twilio Trail Account - www.twilio.com/referral/PfBNJy 
2. Export the following env variables
```
export TWILIO_ACCOUNT_SID="twilio_account_sid" // you will get this here https://www.twilio.com/console
export TWILIO_AUTH_TOKEN="twilio_auth_token" // you will get this here https://www.twilio.com/console
export FROM_MOBILE_NUMBER="twilio_number" // you will get this number after following the steps https://www.twilio.com/console/sms/whatsapp/sandbox
export TO_MOBILE_NUMBER="your_mobile_number"
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
python check_available_slots.py get-state-id --state_name Maharashtra

2. Get the District ID
python check_available_slots.py get-district-id --state_id 21 --district_name Nanded

3. Check available appointment slots district wise
python check_available_slots.py district-wise --district_id 334 -date 10-05-2021

4. Check available appointment slots pincode wise
python check_available_slots.py district-wise -pin 411015 --date 10-05-2021

5. Run the script continously to check for available appointments. This checks after every 5 mins
python check_available_slots.py continuously --district_id 363 --date 10-05-2021
```

Notification will be send on the whatsapp

<img width="634" alt="Screenshot 2021-05-09 at 4 29 01 PM" src="https://user-images.githubusercontent.com/52563354/117569574-f4705780-b0e3-11eb-9967-c09f97e647c5.png">

### TODO
[] Add SMS, Email notification

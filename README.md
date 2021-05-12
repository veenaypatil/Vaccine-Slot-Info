# Vaccine-Slot-Info
CLI to check for Covid Vaccine appointments pincode or district wise and get notified on WhatsApp/Telegram.

### Pre-requisites
1. Python 3.6+ , you can install it from  https://www.python.org/downloads/
2. Either Telegram Account
3. Or Twilio Free Trail Account for whatsapp notification 


### Telegram Bot Configuration
1. On Telegram, search @BotFather, click on START button or send `/start` message
2. Send `/newbot` message and follow the instructions to set the name and username for your bot
3. You will receive a token to access HTTP API, this token is your `TELEGRAM_BOT_TOKEN`
4. Goto your bot name in Telegram and send `/start` message
5. To get your chatId Open a new tab in browser, enter `https://api.telegram.org/bot<token>/getUpdates`
   You will get the response as
    ```
    "ok":true,"result":[{"update_id":334363465,
    "message":{"message_id":3,"from":{"id":130XXXXXX,"is_bot":false,"first_name":"Vinay",
    "language_code":"en"},
    "chat":{"id":130XXXXXX,"first_name":"Vinay","type":"private"},"date":1620703638,"text":"/start",
    "entities":[{"offset":0,"length":6,"type":"bot_command"}]}}]}
    ```
   `TELEGRAM_BOT_CHAT_ID` will be `130XXXXXX` from the above response
6. Export the following env variables on your shell
```
export TELEGRAM_BOT_TOKEN=<from step 3 above>
export TELEGRAM_BOT_CHAT_ID=<from step 5 above>
```

### Twilio Configuration for Whatsapp Notification
1. Create a new Twilio Trail Account - www.twilio.com/referral/PfBNJy 
2. Follow the steps here https://www.twilio.com/console/sms/whatsapp/sandbox
3. Export the following env variables on your shell
```
export TWILIO_ACCOUNT_SID="twilio_account_sid" // you will get this here https://www.twilio.com/console
export TWILIO_AUTH_TOKEN="twilio_auth_token" // you will get this here https://www.twilio.com/console
export FROM_MOBILE_NUMBER="twilio_number" // you will get this number after following the steps https://www.twilio.com/console/sms/whatsapp/sandbox
export TO_MOBILE_NUMBER="your_mobile_number"
```

### Installation steps to use `slotinfo` command

1. Download release directly by clicking on slotinfo-1.0.tar.gz here - https://github.com/veenaypatil/Vaccine-Slot-Info/releases/tag/v1.1
```
sudo pip install <downloaded_folder>/slotinfo-1.0.tar.gz
or 
sudo pip3 install <downloaded_folder>/slotinfo-1.0.tar.gz
```
Checkout how to install pip here - https://www.techgeekbuzz.com/how-to-install-python-pip-on-windows-mac-and-linux/

2. Or Clone the code and install
```
python setup.py sdist
sudo pip install dist/slotinfo-1.0.tar.gz
```

### CLI commands provided by this utility
```
  continuously-for-district
  continuously-for-pincode
  district-wise
  get-district-id
  get-state-id
  pincode-wise
```

### CLI commands usage
```
1. Get the State ID
slotinfo get-state-id --state_name Maharashtra

2. Get the District ID
slotinfo get-district-id --state_id 21 --district_name Pune

3. Check available appointment slots district wise
slotinfo district-wise --district_id 334 --date 10-05-2021 --age_filter 18 --notify_on whatsapp

4. Check available appointment slots pincode wise
slotinfo pincode-wise -pin 411015 --date 10-05-2021 --age_filter 45 --notify_on telegram

5. Run the script continously to check for available appointments in a district after evey x(seconds) interval
slotinfo continuously-for-district --district_id 363 --date 10-05-2021 --age_filter 18 --interval 2 --notify_on telegram

6. Run the script continously to check for available appointments in pin code after evey x(seconds) interval
slotinfo continuously-for-pincode --pin_code 41105 --date 10-05-2021 --age_filter 18 --interval 2 --notify_on whatsapp
```

To get the help of any command use `--help` option with command name
```
slotinfo continuously-for-district --help
Usage: slotinfo continuously-for-district [OPTIONS]

Options:
  -dId, --district_id TEXT        Provide district Id to check for
                                  appointments  [required]

  -d, --date TEXT                 Date for which appointments are to be
                                  checked  [required]

  -af, --age_filter INTEGER       Filter only 18 plus or 45 plus appointments
  -i, --interval INTEGER          Interval in seconds  [required]
  -n, --notify_on [whatsapp|telegram]
                                  Receive notification on whatsapp/telegram
                                  [required]

  --help                          Show this message and exit.
```

### Whatsapp Notification Sample
<img width="350" alt="Screenshot 2021-05-09 at 10 01 03 PM" src="https://user-images.githubusercontent.com/52563354/117579869-927b1680-b112-11eb-9403-21438d53bc46.png">

### Telegram Notification Sample

<img width="657" alt="Screenshot 2021-05-11 at 11 11 05 AM" src="https://user-images.githubusercontent.com/52563354/117764129-9bbacf00-b249-11eb-9609-df53a44ee34d.png">


import smtplib


CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}
carrier = "att"

def send_message(phone_number, message, email, password):
    recipient = phone_number + CARRIERS[carrier]
    auth = (email, password)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(auth[0], auth[1])
 
        server.sendmail(auth[0], recipient, message)
    except Exception as e:
        print('Text did not send successfully')
        print('----------')
        print(e)
import pywhatkit as kit

def send_whatsapp_message(phone_number, message):
    kit.sendwhatmsg_instantly(phone_number, message)

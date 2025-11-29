from twilio.rest import Client

# -------------------------
# TWILIO CREDENTIALS
# -------------------------
account_sid = "ACdc99333f9b49d28e3e2afad3ccbade5b"
auth_token = "4800c0e1f324bf395211a5ba528b5d43"
twilio_number = "+19283823837"  # Twilio number
your_number = "+918015114135"   # Your mobile number

client = Client(account_sid, auth_token)

def send_sms_alert(msg):
    try:
        message = client.messages.create(
            body=msg,
            from_=twilio_number,
            to=your_number
        )
        print("✅ SMS sent:", message.sid)
    except Exception as e:
        print("❌ SMS failed:", e)

# -------------------------
# TEST SMS
# -------------------------
if __name__ == "__main__":
    send_sms_alert("⚠️ ALERT: Intruder detected on your system!")

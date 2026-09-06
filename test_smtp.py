# test_smtp.py

import smtplib

EMAIL = "govscribe.bot@gmail.com"
PASSWORD = "qmxbrwmouprrvebi"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    print("LOGIN BERHASIL")
except Exception as e:
    print("ERROR:")
    print(e)
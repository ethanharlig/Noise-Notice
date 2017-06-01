import smtplib
import datetime

def send_email(is_loud, seconds):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('noisenotice409@gmail.com', 'Greiner409')

    msg = "NoiseNotice has deteced that your sound has been " + ("too loud " if is_loud else "low enough ") + " for " + str(seconds) + " seconds. " + ("Please quiet down." if is_loud else "Party on!")

    carriers = ["@txt.att.net", "@myboostmobile.com", "@mymetropcs.com", "@messaging.sprintpcs.com", "@tmomail.net", "@mms.uscc.net", "@vtext.com", "@vmobl.com"]

    with open('addresses.txt', 'r') as f:
        plain = f.readlines()

    nums = []
    for p in plain:
        nums.append(p.rstrip('\n'))

    for num in nums:
        if "@" not in num:
            for carrier in carriers:
                server.sendmail("Noise Notice", num + carrier, msg)
        else:
            server.sendmail("Noise Notice", num, msg)
        print("Sent a text to %s at %s" % (num, datetime.datetime.now()))


    server.quit()


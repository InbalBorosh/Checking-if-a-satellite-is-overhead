import requests
from datetime import datetime
import smtplib
import sched, time

MY_LAT = 32.073582
MY_LONG = 34.788052

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

def position_relation(MY_LAT, MY_LONG, iss_latitude, iss_longitude):
    if abs(MY_LAT - iss_latitude) <= 5:
        if abs(MY_LONG - iss_longitude) <= 5:
            return True
        else:
            return False
    else:
        return False

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

def sending_mail(scheduler):
    scheduler.enter(60, 1, sending_mail, (scheduler,))
    my_email = "inbal.borosh@gmail.com"
    password = "123456"
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs="inbal.borosh@gmail.com",
                        msg=f"subject: THE ISS IS CLOSE\n\n The ISS's location is {iss_longitude, iss_latitude}. LOOK UP!!")
    connection.close()

if position_relation(MY_LAT, MY_LONG, iss_latitude, iss_longitude):
    if time_now >= sunset or time_now <= sunrise:
        my_scheduler = sched.scheduler(time.time, time.sleep)
        my_scheduler.enter(60, 1, sending_mail, (my_scheduler,))
        my_scheduler.run()


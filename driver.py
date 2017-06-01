import time
from send_email import send_email
import subprocess

def driver_function():
    ndx = 0
    is_loud = False
    seconds_loud = 0
    seconds_quiet = 0
    max_time_loud = 3

    set_lights([(17,255), (22,255), (24,255)])

    while True:
        data = subprocess.check_output("gpio -g read 5", shell=True)
        print(data)

        if int(data) > 0:
            seconds_quiet = 0
            seconds_loud += 1

            if seconds_loud >= max_time_loud and not is_loud:
                is_loud = True
                send_email(is_loud, seconds_loud)
                toggle_lights(is_loud)

        else:
            seconds_loud = 0
            seconds_quiet += 1

            if seconds_quiet >= max_time_loud and is_loud:
                is_loud = False
                send_email(is_loud, seconds_quiet)
                toggle_lights(is_loud)

        print("Seconds quiet: " + str(seconds_quiet))
        print("Seconds loud: " + str(seconds_loud))
        time.sleep(1)


def toggle_lights(is_loud):
    if is_loud:
        set_lights([(17,255), (22,0), (24,0)])
        print("Notifying too loud!")
    else:
        set_lights([(17,0), (22,255), (24,0)])
        print("Notifying quiet enough!")


def set_lights(all_pins):
    for pin in all_pins:
        subprocess.call("pigs p " + str(pin[0]) + " " + str(pin[1]), shell=True)


def config_pins():
    subprocess.call("sudo pigpiod", shell=True)
    subprocess.call("gpio -g mode 17 pwm", shell=True)
    subprocess.call("gpio -g mode 22 pwm", shell=True)
    subprocess.call("gpio -g mode 24 pwm", shell=True)
    subprocess.call("gpio -g mode 5 input", shell=True)


if __name__ == '__main__':
    config_pins()
    driver_function()


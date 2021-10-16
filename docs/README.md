# Raspberry Pi Applicance Notifications

This Raspberry Pi will monitor various home appliances to send you SMS notifications when their cycle has began or ended. This specific build is geared towards a household of four users, but can easily be adapted to accomodate a different number.

It works by utilizing a vibration sensor to detect when an appliance is running or not. In turn, this allows for simply sticking the device to the appliance to get it working, resulting in a damage-free integration.

This project was inspired by [Shmoopty's Appliance Monitor](https://github.com/Shmoopty/rpi-appliance-monitor). Their implementation deals with only notifying one user, so if it this route you wish to take, I reccomend following that repo instead as it will save you time. In my case, however, I have three other roommates that I live with, so having the notifications be sent to only one person would not suffice. To get around this, I built upon Shmoopty's work to add support for buttons, LED's, and a couple of other things.

## How the Code Works

In this build, there are four buttons to choose from, each corresponding to a specific user. When a user presses their assigned button, the program then begins to listen to detected vibrations. When a vibration is detected for a certain amount of consecutive time, it will consider the appliance running. An SMS message will then be sent to the user, notifying them that the device has recognized the appliance as started. The appliance will not be considered done until there have been no vibrations detected for a specified amount of time. Once done, another SMS message will be sent to the user to inform them that the appliance has finished its cycle.

My situation consist of a washer and dryer stacked on top of each other. Because of this, vibrations from one appliance often bleed over into the other. To combat such problem, there is a max time constraint that will automatically consider the appliance done once the specified amount of time has passed, no matter the vibration status. Getting a notification that your laundry is done five minutes late is better than forgetting for hours.

All constraints disussed are open to customization.

## Needed Parts

- Any **Raspberry Pi** (I am using the [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)) If WiFi capability isn't built in, you'll also have to get a USB WiFi dongle.
- **MicroSD Card**
- **Vibration Sensor Module**. I am using an [SW-420 module](https://www.amazon.com/gp/product/B00HJ6ACY2/), but something like an [801s module](https://www.amazon.com/Vibration-Vibrating-Arduino-Adjustable-Sensitivity/dp/B0981DZV6L/) will work as well.
- **Buttons**
- **LEDs**. I am using four red LEDs for the user selection and one blue LED for status indication.
- **microUSB Power Source**

![Raspberry Pi With Case](/images/pi.jpg)

![Parts](/images/parts.jpg)

It is assumed that you have, and are familiar with, the basic tools and materials commonly used when working in the genre of small electronics such as wire, soldering gun, etc. If you are new to this sort of thing, I encourage you to explore the thousands of resources on this topic. Here are a few i've ran into before:

- [Getting Started with Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started)
- [Beginners Guide to Wiring Things to the GPIO](https://forums.raspberrypi.com/viewtopic.php?t=216304)
- There are some great starter kits I have found on Amazon that provide you with almost everything you need to get started, like this [Raspberry Pi Zero W Starter Kit](https://www.amazon.com/gp/product/B0748M1Z1B/) or this [Electronics Fun Kit](https://www.amazon.com/gp/product/B07WL87KHB/)

## Setting Up

First, make sure that you have the [OS installed](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2) on your pi. If you are doing a fresh install of Raspberry Pi OS and do not plan on connecting a monitor and keyboard, make sure to do the following before ejecting the SD card:

- Add an empty file named `ssh` to the boot partition of the SD card to enable `ssh` connections.
- Edit `/etc/hostname` and `/etc/hosts` to change `raspberrypi` to a unique host name, like `laundrypi` (this is optional but highly reccomended).
- Edit `/etc/wpa_supplicant/wpa_supplicant.conf` to add your WiFi network:

```
country=your_country_abbreviation
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
 scan_ssid=1
 ssid="Your WiFi name (SSID)"
 psk="Your WiFi password"
}
```

Otherwise, this configuration can all be done on the booted pi itself, once connected to a monitor and keyboard:

- `ssh` can be enabled by navigating to **Preferences > Raspberry Pi Configuration > Interfaces**.
- Similarly, the hostname can be changed by navigating to **Preferences > Raspberry Pi Configuration** (if not already changed on first boot setup wizard)
- WiFi can be connected through the WiFi symbol located at the top right corner of the screen.

For further instruction on how to actually use `ssh` to connect to your pi, take a look [here](https://itsfoss.com/ssh-into-raspberry/) (even if connected via monitor and keyboard, this will be especially useful whenever you need to control your device in its final mounted position).

## Download and Configure Code

To download the code onto your pi, simply use the `wget` terminal command in your desired directory.

```bash
$ wget https://github.com/Panda64/appliance-notifications/blob/master/main.py?raw=true
$ wget https://github.com/Panda64/appliance-notifications/blob/master/requirements.txt?raw=true
```

Make sure to install the essential libraries:

```bash
$ sudo apt-get install python-pip
$ sudo pip install -r requirements.txt
```

Additionally, if you haven't already, ensure the proper timezone setting for correct timestamps.

```bash
$ sudo raspi-config
[Internationalisation Options]
[Change Timezone]
```

`main.py` uses environment variables, which means you will need to create a `.env` file to define those variables. In the project's current state, the newly created `.env` should look something like this:

```.env
TWILIO_ACCOUNT_SID=sid_here
TWILIO_AUTH_TOKEN=token_here
USER1_START_MESSAGE="User1, your laundry cycle has started. You will be notified when it's complete."
USER2_START_MESSAGE="User2, your laundry cycle has started. You will be notified when it's complete."
USER3_START_MESSAGE="User3, your laundry cycle has started. You will be notified when it's complete."
USER4_START_MESSAGE="User4, your laundry cycle has started. You will be notified when it's complete."
USER1_END_MESSAGE="User1, your laundry is done."
USER2_END_MESSAGE="User2, your laundry is done."
USER3_END_MESSAGE="User3, your laundry is done."
USER4_END_MESSAGE="User4, your laundry is done."
USER1_NUMBER=+19998887777
USER2_NUMBER=+19998887777
USER3_NUMBER=+19998887777
USER4_NUMBER=+19998887777
TWILIO_PHONE_NUMBER=+19998887777
```

This is a good time to point out that because the SMS messages are being sent through [Twilio's](https://www.twilio.com) API, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER` are required fields for the program to run. You can sign up for a Twilio account to obtain this information. If you do not wish to use this service, simply delete the Twilio variables in `main.py` (lines 60-63) and replace the `send_sms()` function with a notification method of your choosing.

After your `.env` file is all setup, make sure your `dotenv_path` in `main.py` (line 10) is properly pointing to it to avoid errors:

```python
load_dotenv(dotenv_path="/path/to/.env")
```

## Connecting the Hardware

Now it's time to setup the hardware. Here is the basic rundown:

- Buttons
  - Connect each to ground and general GPIO port.
- LEDs
  - Connect each to ground and general GPIO port.
  - It is reccomended that each LED have a resistor connected to the positive end as well. In my build, I used 220Ω resistors.
- Vibration Module
  - Connect to power, ground, and GPIO port.
  - Most modules will have their leads labeled.

In order to save on connection points, I reccommend consolidating negatives together (i.e all buttons share a negative wire etc.)

I also advise using a breadboard to prototype your circuit with the code to ensure everything is working properly before thinking of permanent connections. This will save you a bunch of time after everything is soldered together.

![Prototying With Breadboard](/images/breadboard.jpg)

![Final Testing](/images/final_testing.jpg)

## Mounting

Mounting can be done in a variety of ways depending on how you wired everything up as well as what appliance you are dealing with. I didn't have a 3D printer handy for this project, so I just taped and glued it to the side of my washer for now. I plan on making this look much neater in the future.

![Mounted Device](/images/mounted.jpg)

## Fine Tuning

### Parameters

There are a few variables that can be changed to fine tune the performance of this program. See default values below (lines 44-53 of `main.py`):

```python
# Seconds a continuous vibration is detected before the appliance is considered running
begin_seconds = 10
# Seconds no vibration is detected before appliance is considered off
end_seconds = 180
# Max amount of seconds an appliance should be running for
max_time = 5400
# Seconds until user is cleared from being active if the appliance has not started yet
user_expiration = 180
# Debug Messages
verbose = True
```

### Vibration Module

From my experience, these vibration modules can be quite touchy. To adjust the sensitivity, play with the potentiometer located on the module. You can most likely adjust it with a phillips head screwdriver. Additionally, I have found that the module is much more sensitive to vibrations in the vertical direction relative to it being in a portrait orientation. Play around with it and see what works best for you.

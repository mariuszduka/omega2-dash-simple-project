# Omega2 Dash Simple Project

The project shows in a simple way how you can use the Omega2 Dash to manage the electrical circuit. The project uses the LittleV Graphics Library for the Micropython language. Omega2 Pro reads the temperature value from the sensor and, using the Relay Expanson module, enables switching the voltage in the circuit. Omega2 Dash communicates with the Omega2 Pro using socket connections.

version: **1.0.0**

![Omega2 Dash Simple Project](https://github.com/mariuszduka/omega2-dash-simple-project/blob/main/images/o2dash-simple-project.jpg?raw=true "Omega2 Dash Simple Project")

## About Omega2 Dash

The **Omega2 Dash** brings touchscreen capability to the Omega2 Linux computer platform. It is a stand-alone, Wi-Fi-enabled, all-in-one solution for providing touch-based visual UIs that can be internet-connected, connected to other devices, or both. It can display the commandline, run programs that create a touch-based UI, and display images (png, jpeg).

The **Omega2 Pro** is the next generation of Omega2 and the most powerful IoT computer Onion Corporation made yet. It is a standalone device - the processor, memory, gigabytes of storage, and Wi-Fi are all built-in, and it's smaller than a breadboard.

## Requirements

 * Omega2 Dash
 * Omega2(+) plugged into Expansion Dock or Omega2 Pro
 * RFID & NFC Expansion (optional)
 * Relay Expansion (optional)
 * DS18B20 Temperature Sensor
 * 1x LED
 * 1x 220Ω, 1x 5.1kΩ Resistor
 * 5x Jumper wires (M-M)

## Building the Circuit

<img src="https://github.com/mariuszduka/omega2-dash-simple-project/blob/main/images/o2p-relay-o2dash-nfc.jpg?raw=true" width="30%" alt="Omega2+, Omega2 Dash, Relay Expansion"></img>
<img src="https://github.com/mariuszduka/omega2-dash-simple-project/blob/main/images/o2p-relay.jpg?raw=true" width="30%" alt="Omega2+, Relay Expansion"></img>
<img src="https://github.com/mariuszduka/omega2-dash-simple-project/blob/main/images/o2dash-nfc.jpg?raw=true" width="30%" alt="Omega2 Dash, RFID & NFC Expansion"></img>   

**1-Wire temperature sensor**

* With the front of the sensor facing the middle gap of the breadboard, insert the three pins across 3 adjacent rows.
* Connect the 5.1kΩ resistor to both DQ (pin 2) and Vdd (pin 3).
* Connect GND (pin 1) to the Omega’s GND pin.
* Connect DQ (pin 2) to the Omega’s GPIO0.
* Connect Vdd (pin 3) to the Omega’s 3.3V pin.

**LED**

* Plug in the LED into the breadboard, make sure you plug the anode and cathode into different rows and that you know which is plugged where.
* Now connect one end of a 220Ω resistor to the the cathode row, and the other end to an empty row.
* Connect the other end of the resistor to a Ground pin on the Omega2.
* If you use Relay Expansion, connect the the LED’s anode as in the picture, if not, then connect a jumper wire from GPIO1 to the LED’s anode.

## Installation

**Omega2 Dash**

[Enable the Official OpenWRT Package Repos.](https://docs.onion.io/omega2-docs/using-opkg.html) It’s very straightforward to configure opkg to use the OpenWRT package repos in addition to the Onion package repos. This can be accomplished by editing the ```/etc/opkg/distfeeds.conf``` file that configures which repos are to be used.

After setting up your OpenWRT package repositories, install LittleV Graphics Library for Micropython:

```
opkg update
opkg install lv_micropython
opkg install micropython-lib --nodeps
```

Disable the blinking cursor on the display, execute the command:

```
echo 0 > /sys/class/graphics/fbcon/cursor_blink
```

Optionally, you can add the above command to the ```/etc/rc.local``` script.

If you want to use the RFID & NFC Expansion, execute the command:
```
opkg install nfc-exp
```

Download the repo:
```
opkg install git git-http ca-bundle
git clone https://github.com/mariuszduka/omega2-dash-simple-project
```

**Omega2(+) or Omega2 Pro**

```
opkg update
opkg install python3-light
opkg install python3-logging
```

If you want to use the Relay Expansion and switch the voltage in the circuit, execute the command:

```
opkg install python3-relay-exp
```

If you don't have Relay Expansion, the voltage will be changed by the GPIO.

Download the repo:
```
opkg install git git-http ca-bundle
git clone https://github.com/mariuszduka/omega2-dash-simple-project
```

Done!

## Configuration

On Omega2 Dash open the file ```remote.py``` in the directory ```omega2-dash-simple-project/o2dash``` and insert the IP address of Omega2(+) or Omega2 Pro:

```
host = '0.0.0.0'
```

If you are using the RFID & NFC Expansion add the registered NFC card uids to the file ```access.json``` in the directory ```omega2-dash-simple-project/o2dash```.
First check the UID number of the NFC card, execute the command:

```
nfc-list
```

An example of the result of the command running:

```
nfc-list uses libnfc reboot-7475-ge6757b4765
NFC device: Omega NFC Expansion opened
1 ISO14443A passive target(s) found:
ISO/IEC 14443A (106 kbps) target:
    ATQA (SENS_RES): 00  44
       UID (NFCID1): 04  fc  83  32  ed  4c  80
      SAK (SEL_RES): 00
```

Add the UID number to the ```access.json``` file (for example):

```
{ 
	"uids": 
	[ 
		"04fc8332ed4c80", 
		"04068332ed4c81" 
	]
}
```

Done!

## Usage

On **Omega2 Dash**, execute the command:

```
cd omega2-dash-simple-project/o2dash
micropython start.py
```

On **Omega2(+)** or **Omega2 Pro**, execute the command:

```
cd omega2-dash-simple-project/o2pro
python3 sensor.py
```

Done!

## Resources

 * [Omega2 and LED](https://docs.onion.io/omega2-starter-kit/starter-kit-blinking-led.html)
 * [Omega2 and 1-Wire Temperature Sensor](https://docs.onion.io/omega2-starter-kit/starter-kit-temp-sensor.html)
 * [Using the RFID & NFC Expansion](https://docs.onion.io/omega2-docs/using-rfid-nfc-expansion.html)
 * [Using the Relay Expansion](https://docs.onion.io/omega2-docs/using-relay-expansion.html)
 * [Onion Omega2 Dash](https://onion.io/omega2-dash-guide/)
 * [Onion Omega2 Pro](https://docs.onion.io/omega2-docs/omega2-pro.html)
 * [LittleV Graphics Library for Micropython](https://docs.lvgl.io/v7/en/html/get-started/micropython.html)

## License

MIT License

Copyright (c) 2020 Mariusz Duka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
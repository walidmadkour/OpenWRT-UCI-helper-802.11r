# OpenWRT 802.11r FT roaming helper script

EX:- 

## Madkour-Server# python3 helper.py 0 --ap 11:22:33:44:55:00 --ap 11:22:33:44:55:01 --ap 11:22:33:44:55:

This script just simplifies the bootstrap process of creating the `r0kh` and `r1kh` config options.

## Usage

```
usage: helper.py [-h] [--ap AP] [--format {uci,config}] iface

positional arguments:
  iface                 uci wifi iface index
                        you can obtain the uci index by looking for your ssid:
                          uci get wireless.@wifi-iface[0].ssid
                          uci get wireless.@wifi-iface[1].ssid
                          ...

optional arguments:
  -h, --help            show this help message and exit
  --ap AP               bssid(s) of access point(s)
  --format {uci,config}
                        output format
                          uci: prints uci commands (default)
                          config: prints config file snippets
```

So in case you do have 3 access points sharing a SSID all over your place (Notice that there should be only one DHCP server in the network. The APs must not provide their own subnets. (Thanks [khmtambi](https://www.reddit.com/user/khmtambi) for the tip.)), just collect their BSSIDs (In LUCI, go to "Network -> Wireless" and use the BSSID of the SSID you want to provide with roaming) plus the uci wifi index (see usage) and call the script like:

```
./helper.py 0 --ap 11:22:33:44:55:00 --ap 11:22:33:44:55:01 --ap 11:22:33:44:55:02
```

which renders some output with random `mobility_domain` and password for inter-ap radius sessions:

```
Configuration for AP with BSSID 11:22:33:44:55:00:

uci set wireless.@wifi-iface[0].ieee80211r='1'
uci set wireless.@wifi-iface[0].mobility_domain='67c5'
uci set wireless.@wifi-iface[0].pmk_r1_push='1'
uci set wireless.@wifi-iface[0].nasid='112233445500'
uci set wireless.@wifi-iface[0].r1_key_holder='112233445500'
uci set wireless.@wifi-iface[0].r0kh='11:22:33:44:55:00,112233445500,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:01,112233445501,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:02,112233445502,b0b1c207b44819544b07bdc523b2d6db'
uci set wireless.@wifi-iface[0].r1kh='11:22:33:44:55:00,11:22:33:44:55:00,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:01,11:22:33:44:55:01,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:02,11:22:33:44:55:02,b0b1c207b44819544b07bdc523b2d6db'


Configuration for AP with BSSID 11:22:33:44:55:01:

uci set wireless.@wifi-iface[0].ieee80211r='1'
uci set wireless.@wifi-iface[0].mobility_domain='67c5'
uci set wireless.@wifi-iface[0].pmk_r1_push='1'
uci set wireless.@wifi-iface[0].nasid='112233445501'
uci set wireless.@wifi-iface[0].r1_key_holder='112233445501'
uci set wireless.@wifi-iface[0].r0kh='11:22:33:44:55:00,112233445500,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:01,112233445501,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:02,112233445502,b0b1c207b44819544b07bdc523b2d6db'
uci set wireless.@wifi-iface[0].r1kh='11:22:33:44:55:00,11:22:33:44:55:00,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:01,11:22:33:44:55:01,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:02,11:22:33:44:55:02,b0b1c207b44819544b07bdc523b2d6db'


Configuration for AP with BSSID 11:22:33:44:55:02:

uci set wireless.@wifi-iface[0].ieee80211r='1'
uci set wireless.@wifi-iface[0].mobility_domain='67c5'
uci set wireless.@wifi-iface[0].pmk_r1_push='1'
uci set wireless.@wifi-iface[0].nasid='112233445502'
uci set wireless.@wifi-iface[0].r1_key_holder='112233445502'
uci set wireless.@wifi-iface[0].r0kh='11:22:33:44:55:00,112233445500,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:01,112233445501,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:02,112233445502,b0b1c207b44819544b07bdc523b2d6db'
uci set wireless.@wifi-iface[0].r1kh='11:22:33:44:55:00,11:22:33:44:55:00,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:01,11:22:33:44:55:01,b0b1c207b44819544b07bdc523b2d6db 11:22:33:44:55:02,11:22:33:44:55:02,b0b1c207b44819544b07bdc523b2d6db'

Do not forget to save your changes with 'uci commit wireless'

Apply your settings with 'wifi restart'
```

If you like to edit config files instead of uci commands, just change the format:

```
./helper.py 0 --ap 11:22:33:44:55:00 --ap 11:22:33:44:55:01 --ap 11:22:33:44:55:02 --format config


Configuration for AP with BSSID 11:22:33:44:55:00:

	option ieee80211r '1'
	option mobility_domain '3780'
	option pmk_r1_push '1'
	option nasid '112233445500'
	option r1_key_holder '112233445500'
	list r0kh '11:22:33:44:55:00,112233445500,18880d5278d2eb37a744f5ab57bba6fb'
	list r0kh '11:22:33:44:55:01,112233445501,18880d5278d2eb37a744f5ab57bba6fb'
	list r0kh '11:22:33:44:55:02,112233445502,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:00,11:22:33:44:55:00,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:01,11:22:33:44:55:01,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:02,11:22:33:44:55:02,18880d5278d2eb37a744f5ab57bba6fb'


Configuration for AP with BSSID 11:22:33:44:55:01:

	option ieee80211r '1'
	option mobility_domain '3780'
	option pmk_r1_push '1'
	option nasid '112233445501'
	option r1_key_holder '112233445501'
	list r0kh '11:22:33:44:55:00,112233445500,18880d5278d2eb37a744f5ab57bba6fb'
	list r0kh '11:22:33:44:55:01,112233445501,18880d5278d2eb37a744f5ab57bba6fb'
	list r0kh '11:22:33:44:55:02,112233445502,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:00,11:22:33:44:55:00,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:01,11:22:33:44:55:01,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:02,11:22:33:44:55:02,18880d5278d2eb37a744f5ab57bba6fb'


Configuration for AP with BSSID 11:22:33:44:55:02:

	option ieee80211r '1'
	option mobility_domain '3780'
	option pmk_r1_push '1'
	option nasid '112233445502'
	option r1_key_holder '112233445502'
	list r0kh '11:22:33:44:55:00,112233445500,18880d5278d2eb37a744f5ab57bba6fb'
	list r0kh '11:22:33:44:55:01,112233445501,18880d5278d2eb37a744f5ab57bba6fb'
	list r0kh '11:22:33:44:55:02,112233445502,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:00,11:22:33:44:55:00,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:01,11:22:33:44:55:01,18880d5278d2eb37a744f5ab57bba6fb'
	list r1kh '11:22:33:44:55:02,11:22:33:44:55:02,18880d5278d2eb37a744f5ab57bba6fb'

Apply your settings with 'wifi restart'
```

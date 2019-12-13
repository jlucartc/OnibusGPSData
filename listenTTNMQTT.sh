#! /bin/sh

mosquitto_sub -h brazil.thethings.network -t "+/devices/+/up" -u 'bus_gps_data' -P 'ttn-account-v2.AXVZUWtEus1MMpVF8qGf8a7jQEbkU4sUA9sM3WsGkDI' -v >> output20191213_SF9.txt

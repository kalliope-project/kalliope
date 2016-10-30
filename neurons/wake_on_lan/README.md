# wake_on_lan

## Synopsis

Allows a computer to be turned on or awakened from the [WOL](https://en.wikipedia.org/wiki/Wake-on-LAN) protocol by Kalliope.

## Options

| parameter         | required | default         | choices  | comment                                                                                                                                               |
|-------------------|----------|-----------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| mac_address       | yes      |                 |          | Mac address of the target PC to wake up. Accepted format: 'ff.ff.ff.ff.ff.ff', '00-00-00-00-00-00', 'FFFFFFFFFFFF'                                    |
| broadcast_address | no       | 255.255.255.255 |          | Broadcast address where the magic packet will bee sent. By default on most LAN is 255.255.255.255                                                     |
| port              | no       | 9               |          | The magic packet is typically sent as a UDP datagram to port 0,6 7 or 9. This parameter must be an integer. Do not add 'quotes' in your configuration |


## Return Values

None


## Synapses example

Kalliope will send a magic packet to the mac address `00-00-00-00-00-00`
```
- name: "wake-my-PC"
  signals:
    - order: "wake my PC"
  neurons:
    - wake_on_lan:
        mac_address: "00-00-00-00-00-00"
```

If your broadcast address is not 255.255.255.255, or if your ethernet card does not listen on the standard 9 port, you can override default parameters.
In the following example, we suppose that kalliope is on a local areal network 172.16.0.0/16. The broadcast address would be 172.16.255.255.
```
- name: "wake-my-PC"
  signals:
    - order: "wake my PC"
  neurons:
    - wake_on_lan:
        mac_address: "00-00-00-00-00-00"
        broadcast_address: "172.16.255.255"
        port: 7
```

## Notes

> **Note:** The target computer must be on the same local area network as Kalliope.

> **Note:** The target computer must has wake on lan activated in BIOS settings and my be in [OS settings](http://www.groovypost.com/howto/enable-wake-on-lan-windows-10/) too.

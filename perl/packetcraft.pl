#!/usr/bin/perl
# import the Net::RawIP module
use Net::RawIP;

# $raw_net gets a Net::RawIP instance initialized for ICMP
$raw_net = new Net::RawIP({icmp =>{}});

$raw_net -> set(
    {
        ip =>
        {
            # spoof 192.168.0.1 to 192.168.0.200
            # 192.168.0.1 will get echo-replies from 192.168.0.200 without ever sending echo-requests
            saddr => '192.168.0.1',
            daddr => '192.168.0.200'
        },
        icmp =>
        {
            # this is an echo-request
            type => 8,
            # Regular data makes traffic easier to identify when monitoring
            data => "beb39b1d642fc17760f5e40240b9e0cd"
            "0c8326b63a260b2296c4f5ae49210ab4".
            "cc6c727ffa0771192b5fb769b607d027" x 4;
        }
    }
);

# send 5 packets (x), 1 per second (y)
# $raw_net -> send(y,x);

$raw_net -> send(1,5);

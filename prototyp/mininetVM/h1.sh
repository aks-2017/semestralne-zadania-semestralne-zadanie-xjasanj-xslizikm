#!/bin/bash
./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a 10.0.0.5 -c 500 -C 1000 -t 100000 -l sender.log -x reciever.log

#!/usr/bin/python
import time

h5.cmd('./h5.sh &')
h1.cmd('./h1.sh &')
time.sleep(100)
h4.cmd('./h4.sh &')
h3.cmd('./h3.sh &')
time.sleep(100)
h5.cmd('./h5.sh &')
h1.cmd('./h11.sh &')
time.sleep(200)

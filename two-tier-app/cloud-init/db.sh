#!/bin/bash

ip_addr=$(ifconfig eth0 | grep "inet addr:" | cut -d ":" -f2 | cut -d " " -f1)
echo "$ip_addr" > /tmp/hello-world.txt
echo "$db_hostname" >> /tmp/hello-world.txt

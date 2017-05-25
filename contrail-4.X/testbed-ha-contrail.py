# EXAMPLE TESTBED WITH 1 CONTROLLER & 2 COMPUTES

# Author: SAVITHRU LOKANATH
# Contact: SAVITHRU AT JUNIPER.NET
# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.

from fabric.api import env

controller1 = 'root@10.84.18.11'
controller2 = 'root@10.84.18.12'
lb1 = 'root@10.84.18.13'
compute1 = 'root@10.84.18.14'

ext_routers = []

router_asn = 64512

host_build = 'root@10.84.18.11'

env.roledefs = {
    'all': [controller1,controller2,lb1,compute1],
    'contrail-controller': [controller1,controller2],
    'openstack': [controller1],
    'contrail-compute': [compute1],
    'contrail-analytics': [controller1,controller2],
    'contrail-analyticsdb': [controller1,controller2],
    'build': [host_build],
    'contrail-lb': [lb1]
}

env.hostnames = {
    'all': ['a4s16','a4s17','a4s18','a4s19']
}

env.passwords = {
    controller1: 'c0ntrail123',
    controller2: 'c0ntrail123',
    lb1: 'c0ntrail123',
    compute1: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.kernel_upgrade=False

env.openstack = {
    'manage_amqp': "true"
}

env.ha = {
    'contrail_internal_vip': '10.84.18.13',
    'contrail_external_vip': '10.84.18.13',
}

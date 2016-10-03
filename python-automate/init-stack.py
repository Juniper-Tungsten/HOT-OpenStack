#!/usr/bin/env python

#AUTHOR: SAVITHRU LOKANATH
#CONTACT: SAVITHRU AT JUNIPER.NET

import sys, os
from vnc_api import vnc_api
from novaclient.v2 import client

def launch_VM(user, password, project_name, auth_url, vm_name, image_name, flavor_type, network):

        nova = client.Client(user, password, project_name, auth_url, service_type="compute")

        image = nova.images.find(name = image_name)
        flavor = nova.flavors.find(name = flavor_type)
        network = nova.networks.find(label = network)

        nova.servers.create(name=vm_name, image=image.id, flavor=flavor.id, nics=[{'net-id': network.id}])


def create_NetworkPolicy(policy_name, left_network_name, right_network_name, vnc, domain, project_name):

        project = vnc.project_read(fq_name = [domain, project_name])

        rule = vnc_api.PolicyRuleType(direction = '<>', protocol = 'any',
                action_list = vnc_api.ActionListType(simple_action = 'pass'),
                src_addresses = [vnc_api.AddressType(virtual_network = left_network_name)],
                src_ports = [vnc_api.PortType(start_port = -1, end_port = -1)],
                dst_addresses = [vnc_api.AddressType(virtual_network = right_network_name)],
                dst_ports = [vnc_api.PortType(start_port = -1, end_port = -1)])
        policy = vnc_api.NetworkPolicy(name = policy_name, parent_obj = project, network_policy_entries = vnc_api.PolicyEntriesType([rule]))
        
        vnc.network_policy_create(policy)

        print 'Policy "{}" created between "{}" & "{}"\n'.format(policy_name, left_network_name, right_network_name)


def add_NetworkPolicy(policy_name, network, vnc, domain, project_name):

        policy = vnc.network_policy_read(fq_name = [domain, project_name, policy_name])

        policy_type = vnc_api.VirtualNetworkPolicyType(sequence = vnc_api.SequenceType(major = 0, minor = 0))
        vn = vnc.virtual_network_read(fq_name = [domain, project_name, network])
        vn.add_network_policy(ref_obj = policy, ref_data = policy_type)
        
        vnc.virtual_network_update(vn)

        print 'Policy "{}" attached to "{}"\n'.format(policy_name, network)


def create_VirtualNetwork(network_name, network_subnet, network_mask, network_gateway, vnc, domain, project_name):

        """ FUNCTION TO CREATE VIRTUAL-NETWORK """

        project = vnc.project_read(fq_name = [domain, project_name])

        vn_obj = vnc_api.VirtualNetwork(name=network_name, parent_obj=project)
        vn_obj.add_network_ipam(vnc_api.NetworkIpam(),
                        vnc_api.VnSubnetsType([vnc_api.IpamSubnetType(subnet = vnc_api.SubnetType(network_subnet,network_mask), default_gateway = network_gateway)]))


        vnc.virtual_network_create(vn_obj)

        print 'Network "{}" created successfully\n'.format(network_name)

def main():

        """ MAIN/AUTHENTICATE """

        project_name = 'admin'
        domain = 'default-domain'
        username = 'admin'
        password = 'c0ntrail123'
        api_server = '10.84.18.1'
        auth_url = "http://10.84.18.1:5000/v2.0/"

        left_network_name = 'left_VN'
        left_network_subnet = '1.1.1.0'
        left_network_mask = 24
        left_network_gateway = '1.1.1.1'

        right_network_name = 'right_VN'
        right_network_subnet = '2.2.2.0'
        right_network_mask = 24
        right_network_gateway = '2.2.2.1'

        policy_name = 'red-to-blue'

        vnc = vnc_api.VncApi(username=username, password=password, api_server_host = api_server, tenant_name=project_name)

        create_VirtualNetwork(left_network_name, left_network_subnet, left_network_mask, left_network_gateway, vnc, domain, project_name)
        create_VirtualNetwork(right_network_name, right_network_subnet, right_network_mask, right_network_gateway, vnc, domain, project_name)

        create_NetworkPolicy(policy_name, left_network_name, right_network_name, vnc, domain, project_name)
        add_NetworkPolicy(policy_name, left_network_name, vnc, domain, project_name)
        add_NetworkPolicy(policy_name, right_network_name, vnc, domain, project_name)

        launch_VM(username, password, project_name, auth_url, vm_name="vm_1", image_name="ubuntu", flavor_type="m1.tiny", network=left_network_name)
        launch_VM(username, password, project_name, auth_url, vm_name="vm_2", image_name="ubuntu", flavor_type="m1.tiny", network=right_network_name)


if __name__=="__main__":
        main()

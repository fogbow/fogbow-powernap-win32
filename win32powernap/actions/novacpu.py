from novaclient.v1_1 import client
import ConfigParser
import os
import platform

def get_config():
    config = ConfigParser.ConfigParser()
    config.readfp(open('C:\\nova\\nova.conf'))
    return config

def host():
    host = get_config().get('DEFAULT', 'host')
    return host if host is not None else platform.node()

def load_nova_client():
    config = get_config()
    nc = client.Client(
        config.get('keystone_authtoken', 'admin_user'), 
        config.get('keystone_authtoken', 'admin_password'), 
        config.get('keystone_authtoken', 'admin_tenant_name'), 
        '%s://%s:%s/v2.0' % (
            config.get('keystone_authtoken', 'auth_protocol'),
            config.get('keystone_authtoken', 'auth_host'), 
            config.get('keystone_authtoken', 'auth_port')
        ), 
        service_type='compute')
    return nc

class ManageNovaComputeAction:

    def bringup(self):
        nc = load_nova_client()
        host = host()
        search_opts = {'host': host, 'all_tenants': 1}
        server_list = nc.servers.list(search_opts=search_opts)
        for each_server in server_list:
            each_server.stop()

        server_list = nc.servers.list(search_opts=search_opts)
        for each_server in server_list:
            each_server.delete()

        nc.services.disable(host, 'nova-compute')
        nc.services.disable(host, 'nova-network')

    def takedown(self):
        nc = load_nova_client()
        host = host()
        nc.services.enable(host, 'nova-compute')
        nc.services.enable(host, 'nova-network')

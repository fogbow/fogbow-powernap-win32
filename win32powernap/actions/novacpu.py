from novaclient.v1_1 import client
import ConfigParser
import os
import platform

def get_config(conf):
    config = ConfigParser.ConfigParser()
    config.readfp(open(conf['nova_conf_file']))
    return config

def host(conf):
    if not get_config(conf).has_option('DEFAULT', 'host'):
        return platform.node()
    return get_config(conf).get('DEFAULT', 'host')
 
def load_nova_client(conf):
    config = get_config(conf)
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

    def bringup(self, conf):
        nc = load_nova_client(conf)
        auth_host = host(conf)
        search_opts = {'host': auth_host, 'all_tenants': 1}
        server_list = nc.servers.list(search_opts=search_opts)
        for each_server in server_list:
            each_server.stop()

        server_list = nc.servers.list(search_opts=search_opts)
        for each_server in server_list:
            each_server.delete()

        nc.services.disable(auth_host, 'nova-compute')
        nc.services.disable(auth_host, 'nova-network')

    def takedown(self, conf):
        nc = load_nova_client(conf)
        auth_host = host(conf)
        nc.services.enable(auth_host, 'nova-compute')
        nc.services.enable(auth_host, 'nova-network')

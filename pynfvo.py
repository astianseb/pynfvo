#!usr/bin/env python

### Copyright (c) Cisco Systems Inc. 2017
### Author Sebastian Grabski <segrabsk@cisco.com>

from pynso.client import NSOClient
from pynso.datastores import DatastoreType
from pynso.resourcetypes import MediaType
import json

NSO_SERVER = '192.168.23.2'
NSO_API_USERNAME = 'admin'
NSO_API_PASSWORD = 'admin'

VNFR_PATH = '/root/demo/nso/vnfr/'
VNFD_PATH = '/root/demo/nso/vnfd/'

class Nso():

    def __init__(self):
        self.nso_server = NSO_SERVER
        self.nso_api_username = NSO_API_USERNAME
        self.nso_api_password = NSO_API_PASSWORD

        self.nso_handler = NSOClient(self.nso_server, self.nso_api_username, self.nso_api_password)

    def _get_string(self, tenant_name, descriptior_name, esc_name):
        return str(tenant_name) + "," + str(descriptior_name) + "," + str(esc_name)

    def get_api_version(self):
        return self.nso_handler.info()['version']

    def get_nfvo_vnfrs(self):
        return self.nso_handler.get_data(DatastoreType.RUNNING,
                                         ('nfvo', 'vnfr', 'nfvo-esc:esc'),
                                         header='Accept',
                                         media_type=MediaType.DATA,
                                         params='deep')['tailf-nfvo-esc:esc']['vnf-deployment']

    def get_nfvo_vnfr(self, tenant_name, vnfr_name, esc_name):
        return self.nso_handler.get_data(DatastoreType.RUNNING,
                                         ('nfvo', 'vnfr', 'nfvo-esc:esc', 'vnf-deployment',
                                          self._get_string(tenant_name, vnfr_name, esc_name)),
                                         header='Accept',
                                         media_type=MediaType.DATA,
                                         params='deep')['tailf-nfvo-esc:vnf-deployment']

    def get_nfvo_vnfr_status(self, tenant_name, vnfr_name, esc_name):
        return self.nso_handler.get_data(DatastoreType.OPERATIONAL,
                                         ('nfvo', 'vnfr', 'nfvo-esc:esc', 'vnf-deployment',
                                          self._get_string(tenant_name, vnfr_name, esc_name)),
                                         header='Accept',
                                         media_type=MediaType.DATA,
                                         params='deep')['tailf-nfvo-esc:vnf-deployment']

    def create_nfvo_vnfr(self, vnfr_file):

        try:
            with open(VNFR_PATH + vnfr_file) as json_data:
                vnfr = json.load(json_data)

        except:
            return None

        return self.nso_handler.set_data_value(DatastoreType.RUNNING,
                                               ('nfvo', 'vnfr', 'nfvo-esc:esc'),
                                               json.dumps(vnfr),
                                               header='Content-Type')

    def delete_nfvo_vnfr(self, tenant_name, vnfr_name, esc_name):
        return self.nso_handler.delete_path(DatastoreType.RUNNING,
                                         ('nfvo', 'vnfr', 'nfvo-esc:esc', 'vnf-deployment',
                                          self._get_string(tenant_name, vnfr_name, esc_name)),
                                         header='Accept')

    def get_nfvo_vnfds(self):
        return self.nso_handler.get_data(DatastoreType.RUNNING,
                                         ('nfvo', 'vnfd',),
                                         header='Accept',
                                         media_type=MediaType.COLLECTION,
                                         params='deep')['collection']

    def get_nfvo_vnfd(self, vnfd_name):
        return self.nso_handler.get_data(DatastoreType.RUNNING,
                                         ('nfvo', 'vnfd', vnfd_name),
                                         header='Accept',
                                         media_type=MediaType.DATA,
                                         params='deep')

    def create_nfvo_vnfd(self, vnfd_file):

        try:
            with open(VNFD_PATH + vnfd_file) as json_data:
                vnfd = json.load(json_data)

        except:
            return None

        return self.nso_handler.set_data_value(DatastoreType.RUNNING,
                                               ('nfvo', ),
                                               json.dumps(vnfd),
                                               header='Content-Type')

    def delete_nfvo_vnfd(self, vnfd_name):
        return self.nso_handler.delete_path(DatastoreType.RUNNING,
                                            ('nfvo', 'vnfd', vnfd_name),
                                            header='Accept')


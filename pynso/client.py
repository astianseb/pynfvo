# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
The main client class for the NSO APIs
'''
from .connection import NSOConnection
from .resourcetypes import MediaType
from .datastores import DatastoreType

__all__ = ['NSOClient']


class NSOClient(object):
    connectionCls = NSOConnection

    def __init__(self, host, username, password,
                 port=8080, ssl=False):
        self.connection = self.connectionCls('%s:%s' % (host, port),
                                             username,
                                             password,
                                             ssl)

    def info(self):
        """
        Returns API information
        """
        return self.connection.get(resource_type=None,
                                   media_type=MediaType.API,
                                   header='Accept',
                                   path=None)['api']

    def get_datastore(self, datastore, header=None, params=None):
        """
        Get the details of a datastore

        :param datastore: The target datastore
        :type  datastore: :class:`DatastoreType`
        """
        return self.connection.get(resource_type=datastore,
                                   header=header,
                                   media_type=MediaType.DATASTORE,
                                   path=None,
                                   params=params)

    def get_data(self, datastore, data_path, header=None, media_type=None, params=None):
        """
        Get a data entry in a datastore

        :param datastore: The target datastore
        :type  datastore: :class:`DatastoreType`

        :param data_path: The list of paths
        :type  data_path: ``list`` of ``str`` or ``tuple``

        :param header: Header name, mostly "Accept" or "Content-Type"
        :type header: 'str'
        """
        data_path = '/'.join(data_path)
        return self.connection.get(resource_type=datastore,
                                   header=header,
                                   media_type=media_type,
                                   path=data_path,
                                   params=params)

    def set_data_value(self, datastore, data_path, data, header=None, params=None):
        """
        Update (POST) a data entry in a datastore

        :param datastore: The target datastore
        :type  datastore: :class:`DatastoreType`

        :param data_path: The list of paths
        :type  data_path: ``list`` of ``str`` or ``tuple``

        :param data: The new value at the given path
        :type  data: ``dict``

        :param header: Header name, mostly "Accept" or "Content-Type"
        :type header: 'str'

        :rtype: ``bool``
        :return: ``True`` if successful, otherwise error.
        """
        data_path = '/'.join(data_path)
        return self.connection.post(resource_type=datastore,
                                    header=header,
                                    media_type=MediaType.DATA,
                                    path=data_path,
                                    data=data,
                                    params=params)

    def create_data_value(self, datastore, data_path, data, header=None, params=None):
        """
        Create (PUT) a data entry in a datastore

        :param datastore: The target datastore
        :type  datastore: :class:`DatastoreType`

        :param data_path: The list of paths
        :type  data_path: ``list`` of ``str`` or ``tuple``

        :param data: The new value at the given path
        :type  data: ``dict``

        :param header: Header name, mostly "Accept" or "Content-Type"
        :type header: 'str'

        :rtype: ``bool``
        :return: ``True`` if successful, otherwise error.
        """
        data_path = '/'.join(data_path)
        return self.connection.put(resource_type=datastore,
                                   header=header,
                                   media_type=MediaType.DATA,
                                   path=data_path,
                                   data=data,
                                   params=params)

    def delete_path(self, datastore, data_path, header=None, params=None):
        """
        Delete a data entry in a datastore

        :param datastore: The target datastore
        :type  datastore: :class:`DatastoreType`

        :param data_path: The list of paths
        :type  data_path: ``list`` of ``str`` or ``tuple``

        :param header: Header name, mostly "Accept" or "Content-Type"
        :type header: 'str'

        :rtype: ``bool``
        :return: ``True`` if successful, otherwise error.
        """
        data_path = '/'.join(data_path)
        return self.connection.delete(
            resource_type=datastore,
            header=header,
            media_type=MediaType.DATA,
            path=data_path,
            params=params)

    def get_rollbacks(self):
        """
        Get a list of stored rollbacks
        """
        return self.connection.get(resource_type=DatastoreType.ROLLBACKS,
                                   media_type=MediaType.API, header='Accept')

    def get_rollback(self, name):
        """
        Get a list of stored rollbacks
        """
        return self.connection.get_plain(
            resource_type=DatastoreType.ROLLBACKS,
            media_type=MediaType.API,
            header='Accept',
            path=name)

    def apply_rollback(self, datastore, name):
        """
        Apply a system rollback
        """
        return self.connection.post(
            resource_type=datastore,
            media_type=MediaType.DATA,
            header=header,
            path='rollback',
            data={'file': name})

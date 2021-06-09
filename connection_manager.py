
from device_connection import DeviceConnection


class ConnectionManager(object):
    """docstring for ConnectionManager."""

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self.deviceConnections = {}
        self.associatedIP = {}

    def add_device_connection(self, ip, deviceID):
        dev_conn = DeviceConnection(ip, deviceID)
        self.add_device_connection_cpy(dev_conn)

    def add_device_connection_cpy(self, deviceConnection):
        deviceID = deviceConnection.get_deviceID()
        self.deviceConnections[deviceID] = deviceConnection
        self.associatedIP[deviceConnection.get_ip()] = deviceID

    def remove_device_connection(self, deviceID):
        self.deviceConnections.pop(deviceID)

    #def remove_associated_data(self, deviceID):
    #    self.deviceConnections[deviceID].remove_associated_data()

    def find_connection_deviceID(self, deviceID):
        dev_conn = self.deviceConnections.get(deviceID)
        return dev_conn

    def find_connection_ip(self, ip):
        return self.find_connection_deviceID(self.associatedIP[ip])

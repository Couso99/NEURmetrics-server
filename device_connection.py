

class DeviceConnection(object):
    """docstring for DeviceConnection."""

    def __init__(self, ip, deviceID):
        super(DeviceConnection, self).__init__()
        self.ip = ip
        self.deviceID = deviceID
        self.associatedData = {}

    def get_ip(self):
        return self.ip

    def set_ip(self,ip):
        self.ip = ip

    def get_deviceID(self):
        return self.deviceID

    def set_deviceID(self,deviceID):
        self.deviceID = deviceID

    def get_associatedData(self):
        return self.associatedData

    def add_associatedData(self,data):
        self.associatedData.update(data)

    def remove_associated_data(self):
        self.associatedData = {}

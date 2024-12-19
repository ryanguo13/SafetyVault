import pyudev

class udevrunner:
    udevdatabase = None
    device_conectted = None


    def __init__(self):
        """init the udev database in this class"""
        self.udevdatabase = pyudev.Context()
        

    def connect(self, device_dev_path:str):
        """
        Args: device_dev_path: the device path in /dev
        
        this function will connect to the device and set the device_conectted to the device in this class
        """
        self.device_conectted = pyudev.Device.from_device_file(self.udevdatabase, device_dev_path)
        return self.device_conectted
        
    def query_connected_info(self):
        """
        this function will return all information of device_conectted in this class
        same as you running udevadm info -a -n device_dev_path
        """
        parent_device = self.device_conectted
        while parent_device:
            if "ID_SERIAL" in parent_device.properties:
                return parent_device.properties['ID_SERIAL']
            parent_device = parent_device.parent
        else:
            print("未找到包含序列号的设备")
            return "this device don't have ordinary serial number"











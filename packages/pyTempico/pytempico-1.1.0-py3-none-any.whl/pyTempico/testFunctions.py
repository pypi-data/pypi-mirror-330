import serial
from core import TempicoDevice as TempDev
from core import TempicoDevices as TempDevs

#Test for abort measure

# tempicoDevice = TempDev('COM12')
# tempicoDevice.openTempico()
# tempicoDevice.close()
# valueIdn=tempicoDevice.getIdn()
# tempicoDevice.measure()
# #tempicoDevice.abort()
# print(tempicoDevice.fetch())
# tempicoDevice.close()
#change
#change2
#Test for selfTest
# tempicoDevice = TempDev('COM12')
# tempicoDevice.openTempico()
# tempicoDevice.selfTest()
# tempicoDevice.close()

#Test tempico devices
# tempicoDevice = TempDev('COM42')
# portsFound=tempicoDevice.findDevices()
# print(portsFound)

#Test new open function
tempicoDevice = TempDev('COM12')
tempicoDevice.openTempico()
tempicoDevice.close()

# DevTemp=TempDevs()
# devices=DevTemp.findDevices()
# print(devices)